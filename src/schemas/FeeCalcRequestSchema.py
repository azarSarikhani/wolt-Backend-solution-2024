import re
from pydantic import BaseModel, Field,ValidationError
from datetime import  datetime
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator


# def check_pattern(time: str):
#	assert re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d{1,2}Z', time)!=None, f'{time} does not match the pattern \d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ'
#	return(time)



def check_date(time: str):
	assert datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'), f'{time} is not a valid date'
	return (time)
    
def check_year_range(time: str):
	# todo
	pass

customTime = Annotated[str, AfterValidator(check_date)]

class FeeCalcRequestSchema(BaseModel):
	cart_value: float = Field(ge=1, description="Value of the shopping cart in cents.") 
	delivery_distance: int = Field(ge=0, description="The distance between the store and customer’s location in meters.")
	number_of_items: int = Field(ge=1, description="The number of items in the customer's shopping cart.")
	time: customTime = Field(pattern=r"\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d{1,2}Z", description="Order time in UTC in ISO format.")
	class Config:
		json_schema_extra = {
			"example":{
				"cart_value": 790,
				"delivery_distance": 2235,
				"number_of_items": 4,
				"time": "2024-01-15T13:00:00Z"
			}
		}


#try:
#    FeeCalcRequestSchema(cart_value=2, delivery_distance=2,number_of_items=1, time='9999-04-23T13:00:00Z' )
#except ValidationError as e:
#    print(e)

