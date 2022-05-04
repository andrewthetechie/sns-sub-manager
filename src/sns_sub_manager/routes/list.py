from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from ..config import Config
from ..config import SNSConfig
from ..config import get_config
from ..utils.logging import get_logger


list_router = APIRouter(prefix="/sns", tags=["sns"])


@list_router.get("", response_model=List[SNSConfig])
async def get_topics(
    config: Config = Depends(get_config), logger=Depends(get_logger)
) -> List[SNSConfig]:
    """Return the topics managed by this api"""
    return list(config.sns_config.values())


@list_router.get("/{name}", response_model=SNSConfig)
async def get_topic_by_name(
    name: str, config: Config = Depends(get_config), logger=Depends(get_logger)
) -> SNSConfig:
    """Return info about a single topic"""
    topic = config.sns_config.get(name, None)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic
