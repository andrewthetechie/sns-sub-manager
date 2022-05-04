from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Union

from phonenumbers import NumberParseException
from phonenumbers import PhoneNumberType
from phonenumbers import is_valid_number
from phonenumbers import number_type
from phonenumbers import parse as parse_phone_number
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import HttpUrl
from pydantic import constr
from pydantic import validator


MOBILE_NUMBER_TYPES = PhoneNumberType.MOBILE, PhoneNumberType.FIXED_LINE_OR_MOBILE

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


class RequestAttributes(BaseModel):
    FilterPolicy: Optional[Dict[str, Any]] = Field(
        None,
        description="The simple JSON object that lets your subscriber receive "
        "only a subset of messages, rather than receiving every message published to the topic.",
    )


class _RequestDetails(BaseModel):
    ...
    attributes: Optional[RequestAttributes] = Field(
        None, description="Attributes for this subscription request"
    )


class HttpRequestAttributes(RequestAttributes):
    DeliveryPolicy: Optional[Dict[str, Any]] = Field(
        None,
        description="The policy that defines how Amazon SNS retries failed deliveries to HTTP/S endpoints.",
    )
    RawMessageDelivery: bool = Field(
        False,
        description="When set to true , enables raw message delivery to Amazon SQS or HTTP/S endpoints. "
        "This eliminates the need for the endpoints to process JSON formatting, which is otherwise created"
        " for Amazon SNS metadata.",
    )


class HttpRequest(_RequestDetails):
    endpoint: HttpUrl = Field(description="Http/Https endpoint")
    attributes: Optional[HttpRequestAttributes] = Field(
        None, description="Attributes for this http/s subscription request"
    )


class EmailRequest(_RequestDetails):
    endpoint: EmailStr = Field(description="Email to subscribe")


class EmailJsonRequest(EmailRequest):
    ...


class SMSRequest(_RequestDetails):
    endpoint: constr(max_length=50, strip_whitespace=True) = Field(
        None, description="Phone number to subscribe"
    )

    @validator("endpoint")
    def validate_phone_number(cls, v):
        """Uses the phone number library to validate this is a valid phone number"""
        if v is None:
            return v

        try:
            n = parse_phone_number(v, None)
        except NumberParseException as e:
            raise ValueError("Please provide a valid mobile phone number") from e

        if not is_valid_number(n) or number_type(n) not in MOBILE_NUMBER_TYPES:
            raise ValueError("Please provide a valid mobile phone number")

        return v


class SQSRequestAttributes(RequestAttributes):
    RedrivePolicy: Optional[Dict[str, Any]] = Field(
        None,
        description="When specified, sends undeliverable messages to the specified Amazon SQS dead-letter queue. "
        "Messages that can't be delivered due to client errors (for example, when the subscribed endpoint is "
        "unreachable) or server errors (for example, when the service that powers the subscribed endpoint "
        "becomes unavailable) are held in the dead-letter queue for further analysis or reprocessing.",
    )
    RawMessageDelivery: bool = Field(
        False,
        description="When set to true , enables raw message delivery to Amazon SQS or HTTP/S endpoints. This "
        "eliminates the need for the endpoints to process JSON formatting, which is otherwise created for Amazon SNS metadata.",
    )


class SQSRequest(_RequestDetails):
    endpoint: str = Field(description="ARN of SQS Queue to subscribe")
    attributes: Optional[SQSRequestAttributes] = Field(
        description="Attributes for this SQS Subscription request"
    )


class ApplicationRequest(_RequestDetails):
    endpoint: str = Field(description="EndpointArn of a mobile app and device")


class LambdaRequest(_RequestDetails):
    endpoint: str = Field(description="ARN of an Lambda function")


class FirehoseRequestAttributes(RequestAttributes):
    SubscriptionRoleArn: str = Field(
        description="The ARN of the IAM role that has the following: Permission to write to the Kinesis Data "
        "Firehose delivery stream, Amazon SNS listed as a trusted entity"
    )


class FirehoseRequest(_RequestDetails):
    endpoint: str = Field(
        description="ARN of an Amazon Kinesis Data Firehose delivery stream."
    )
    attributes: FirehoseRequestAttributes = Field(
        description="Attributes for this Firehose subscription request"
    )


class SubscribeRequest(BaseModel):
    subscribtion_type: Literal[ALLOWED_SUBSCRIPTIONS] = Field(
        description="What type of subscription is this?"
    )
    subscription_details: Union[
        HttpRequest,
        EmailRequest,
        EmailJsonRequest,
        SMSRequest,
        SQSRequest,
        ApplicationRequest,
        LambdaRequest,
        FirehoseRequest,
    ] = Field(description="Details for this subscription request")


class SubscribeOut(BaseModel):
    subscription_arn: str
    status: str
    details: Optional[List[str]]


class Subscription(BaseModel):
    arn: str
    endpoint: str
    type: Literal[ALLOWED_SUBSCRIPTIONS]
