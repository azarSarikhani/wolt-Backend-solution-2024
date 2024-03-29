from pydantic import BaseModel, Field
from datetime import datetime
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator


def check_date(time: str):
    assert datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'), f'{time} is not a valid date'
    return (time)


customTime = Annotated[str, AfterValidator(check_date)]


class FeeCalcRequestSchema(BaseModel):
    cart_value: int = Field(ge=1, description="Value of the shopping cart in cents.")
    delivery_distance: int = Field(
        ge=0,
        description="The distance between the store and customer’s location in meters."
    )
    number_of_items: int = Field(
        ge=1,
        description="The number of items in the customer's shopping cart."
    )
    time: customTime = Field(
        pattern=r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d{1,2}Z",
        description="Order time in UTC in ISO format."
    )
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "cart_value": 790,
                "delivery_distance": 2235,
                "number_of_items": 4,
                "time": "2024-01-15T13:00:00Z"
            }]
        }
    }
