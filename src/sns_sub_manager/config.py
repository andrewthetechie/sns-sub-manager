import os
from functools import lru_cache
from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

import yaml
from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import Field
from pydantic import validator


class Config(BaseSettings):
    log_level: str = "info"
    app_name: str = "sns-sub-manager"

    sns_config_file: str = "./sns-config.yaml"
    do_not_delete: bool = False

    # cors
    enable_cors: bool = True
    cors_allow_credentials: bool = True
    cors_allow_methods: List[str] = ["*"]
    cors_allow_headers: List[str] = ["*"]
    cors_max_age: int = 90
    cors_origins: List[str] = ["*"]
    cors_origin_regex: Optional[str] = None

    @property
    def sns_config(self) -> Dict[str, Any]:
        return load_sns_yaml(self.sns_config_file)

    @property
    def log_dict_config(self):
        """A logging dict config used to configure logging"""
        return {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "()": "uvicorn.logging.DefaultFormatter",
                    "fmt": "%(levelprefix)s %(asctime)s [%(filename)s:%(lineno)s %(funcName)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                self.app_name: {
                    "handlers": ["default"],
                    "level": self.log_level.upper(),
                },
            },
        }

    class Config:
        """Pydantic base setting config"""

        env_prefix = os.environ.get("CONFIG_PREFIX", "")


ALLOWED_SUBSCRIPTIONS = (
    "http",
    "https",
    "email",
    "email-json",
    "sms",
    "sqs",
    "application",
    "lambda",
    "firehose",
)


class SNSConfig(BaseModel):
    arn: str = Field(description="ARN of the topic")
    name: Optional[str] = Field(
        None,
        description="Optional name of the arn, if not passed will derive from the arn",
    )
    allowed_subscriptions: Optional[List[Literal[ALLOWED_SUBSCRIPTIONS]]] = Field(
        list(ALLOWED_SUBSCRIPTIONS), description="List of allowed subscription types"
    )

    @validator("arn")
    def validate_arn(cls, value):
        arn_split = value.split(":")
        if len(arn_split) != 6:
            raise ValueError("Invalid arn")
        if arn_split[0] != "arn":
            raise ValueError("Invalid arn")
        if arn_split[1] != "aws":
            raise ValueError("Invalid arn")
        if arn_split[2] != "sns":
            raise ValueError("Invalid arn")
        if not arn_split[4].isnumeric():
            raise ValueError("Invalid arn")
        return value

    @validator("name", always=True, pre=True)
    def validate_name(cls, value, values):
        if value is None or value == "":
            return values["arn"].split(":")[-1]
        return value

    @property
    def region(self):
        return self.arn.split(":")[3]

    @property
    def account(self):
        return self.arn.split(":")[4]


@lru_cache
def load_sns_yaml(file_path: str) -> Dict[str, SNSConfig]:
    with open(file_path) as fh:
        loaded = yaml.safe_load(fh)
    to_return = {}
    for sns_dict in loaded["topics"]:
        this_config = SNSConfig(**sns_dict)
        if this_config.name in to_return:
            raise InvalidSnsConfigError(
                f"{this_config.name} already exists with arn {to_return[this_config.name].arn}"
            )
        to_return[this_config.name] = this_config
    return to_return


@lru_cache()
def get_config() -> Config:
    """Gets a config object from the env and returns it
    LRU cached so subsequent calls don't have to do the env lookups
    Returns:
        Config -- config object
    """
    return Config()


class InvalidSnsConfigError(Exception):
    pass
