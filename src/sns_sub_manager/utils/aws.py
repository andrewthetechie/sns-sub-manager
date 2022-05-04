import os
from typing import Any
from typing import Dict
from typing import List

from aiobotocore.session import AioSession
from aiobotocore.session import get_session


# This is a list of service names we can emulate with localstack during local testing and CI
LOCALSTACK_SERVICES = (
    os.environ.get("LOCALSTACK_SERVICES", "sqs,sns").lower().split(",")
)
LOCALSTACK_PROFILE = os.environ.get("LOCALSTACK_PROFILE", "localstack")
LOCALSTACK_ENDPOINT = os.environ.get("LOCALSTACK_ENDPOINT_URL", "http://localhost:4566")


def get_aws_client(region: str, client_type: str):
    if client_type in LOCALSTACK_SERVICES and LOCALSTACK_ENDPOINT != "":
        return _get_localstack_client(region, client_type)
    else:
        session = get_session()
        return session.create_client(client_type, region_name=region)


def _get_localstack_client(region: str, client_type: str):
    session = AioSession()
    session.set_credentials("test", "test")
    return session.create_client(
        client_type, region_name=region, endpoint_url=LOCALSTACK_ENDPOINT
    )


async def subscribe_to_topic(
    region: str,
    topic_arn: str,
    subscription_type: str,
    endpoint: str,
    **subscription_attributes,
) -> Dict[str, Any]:
    """Trigger a subscription to a SNS topic via the aws api

    Args:
        region (str): [description]
        topic_arn (str): [description]
        subscription_type (str): [description]
        endpoint (str): [description]

    Returns:
        str: subscription arn
    """
    async with get_aws_client(region=region, client_type="sns") as sns_client:
        try:
            response = await sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol=subscription_type,
                Endpoint=endpoint,
                Attributes=subscription_attributes,
                ReturnSubscriptionArn=True,
            )
        except sns_client.exceptions.SubscriptionLimitExceededException as exc:
            raise SNSExceptionError(
                f"SubscriptionLimitExceededException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.FilterPolicyLimitExceededException as exc:
            raise SNSExceptionError(
                f"FilterPolicyLimitExceededException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InvalidParameterException as exc:
            raise SNSExceptionError(
                f"InvalidParameterException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InternalErrorException as exc:
            raise SNSExceptionError(
                f"InternalErrorException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.NotFoundException as exc:
            raise SNSExceptionError(
                f"NotFoundException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.AuthorizationErrorException as exc:
            raise SNSExceptionError(
                f"AuthorizationErrorException: while subscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InvalidSecurityException as exc:
            raise SNSExceptionError(
                f"InvalidSecurityException: while subscribing {exc.msg}"
            ) from exc
    return response


async def unsubscribe_from_topic(region: str, subscription_arn: str) -> None:
    """Unsubscribe from a SNS topic

    Args:
        region (str): [description]

    Returns:
    """
    async with get_aws_client(region=region, client_type="sns") as sns_client:
        try:
            await sns_client.unsubscribe(
                SubscriptionArn=subscription_arn,
            )
        except sns_client.exceptions.InvalidParameterException as exc:
            raise SNSExceptionError(
                f"InvalidParameterException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InternalErrorException as exc:
            raise SNSExceptionError(
                f"InternalErrorException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.AuthorizationErrorException as exc:
            raise SNSExceptionError(
                f"AuthorizationErrorException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.NotFoundException as exc:
            raise SNSExceptionError(
                f"NotFoundException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InvalidSecurityException as exc:
            raise SNSExceptionError(
                f"InvalidSecurityException: while unsubscribing {exc.msg}"
            ) from exc


async def get_topic_subscriptions(region: str, topic_arn: str) -> List[Dict[str, Any]]:
    """Get a topics subscriptions

    Args:
        region (str): [description]
        topic_arn (str): [description]

    Returns:
        List[Dict[str, Any]]: [description]
    """
    to_return = []
    async with get_aws_client(region=region, client_type="sns") as sns_client:
        try:
            paginator = sns_client.get_paginator("list_subscriptions_by_topic")
            async for response in paginator.paginate(
                TopicArn=topic_arn,
            ):
                to_return += response["Subscriptions"]
        except sns_client.exceptions.InvalidParameterException as exc:
            raise SNSExceptionError(
                f"InvalidParameterException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.InternalErrorException as exc:
            raise SNSExceptionError(
                f"InternalErrorException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.AuthorizationErrorException as exc:
            raise SNSExceptionError(
                f"AuthorizationErrorException: while unsubscribing {exc.msg}"
            ) from exc
        except sns_client.exceptions.NotFoundException as exc:
            raise SNSExceptionError(
                f"NotFoundException: while unsubscribing {exc.msg}"
            ) from exc
    return to_return


class SNSExceptionError(Exception):
    pass
