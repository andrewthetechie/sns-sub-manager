from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from ..config import Config
from ..config import SNSConfig
from ..config import get_config
from ..schemas.subscribe import SubscribeOut
from ..schemas.subscribe import SubscribeRequest
from ..schemas.subscribe import Subscription
from ..utils.aws import SNSExceptionError
from ..utils.aws import get_topic_subscriptions
from ..utils.aws import subscribe_to_topic as sub_to_topic
from ..utils.aws import unsubscribe_from_topic
from ..utils.logging import get_logger


sub_router = APIRouter(prefix="/sns", tags=["sns"])


@sub_router.post("/{name}/sub", response_model=SubscribeOut)
async def subscribe_to_topic(
    name: str,
    sub_req: SubscribeRequest,
    config: Config = Depends(get_config),
    logger=Depends(get_logger),
) -> SNSConfig:
    """Subscribe to a topic"""
    topic = config.sns_config.get(name, None)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    try:
        if sub_req.subscription_details.attributes is None:
            response = await sub_to_topic(
                topic.region,
                topic.arn,
                sub_req.subscribtion_type,
                sub_req.subscription_details.endpoint,
            )
        else:
            response = await sub_to_topic(
                topic.region,
                topic.arn,
                sub_req.subscribtion_type,
                sub_req.subscription_details.endpoint,
                **sub_req.subscription_details.attributes.dict(),
            )
    except SNSExceptionError as exc:
        logger.exception(
            "Exception when subscribing to %s - %s - %s", name, sub_req, exc
        )
        raise HTTPException(
            status_code=500, detail=f"Error when subscribing to SNS {exc.msg}"
        ) from None
    return SubscribeOut(subscription_arn=response["SubscriptionArn"], status="ok")


@sub_router.get("/{name}/sub", response_model=List[Subscription])
async def get_subscriptions(
    name: str, config: Config = Depends(get_config), logger=Depends(get_logger)
) -> List[Subscription]:
    """Get subscriptions for a topic"""
    topic = config.sns_config.get(name, None)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    try:
        subs = await get_topic_subscriptions(topic.region, topic.arn)
    except SNSExceptionError as exc:
        logger.exception(
            "Exception when trying to get subscriptions for %s - %s", name, exc
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error when trying to get subscriptions for SNS {exc.msg}",
        ) from None
    return [
        Subscription(
            arn=sub["SubscriptionArn"], endpoint=sub["Endpoint"], type=sub["Protocol"]
        )
        for sub in subs
    ]


@sub_router.delete("/{name}/sub/{sub_arn}")
async def delete_subscription(
    name: str,
    sub_arn: str,
    config: Config = Depends(get_config),
    logger=Depends(get_logger),
):
    """Delete a subscription from a topic"""
    if config.do_not_delete:
        raise HTTPException(status_code=501, details="Unsubscribe is not enabled")
    topic = config.sns_config.get(name, None)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    try:
        await unsubscribe_from_topic(topic.region, sub_arn)
    except SNSExceptionError as exc:
        logger.exception(
            "Exception when unsubscribing %s from %s - %s", sub_arn, name, exc
        )
        raise HTTPException(
            status_code=500, detail=f"Error when unsubscribing from SNS {exc.msg}"
        ) from None
    return {}
