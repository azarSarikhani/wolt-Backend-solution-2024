import re
from pydantic import BaseModel, Field,ValidationError
from datetime import  datetime
from typing_extensions import Annotated
from pydantic.functional_validators import AfterValidator

def check_pattern(time: str):
	assert re.match(r'\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ', time)!=None, f'{time} does not match the pattern \d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\dZ'
	return(time)




def check_date(time: str):
	assert datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ'), f'{time} is not a valid date'
	return (time)
    
def check_year_range(time: str):
	# todo
	pass

customTime = Annotated[str, AfterValidator(check_pattern), AfterValidator(check_date)]

class FeeCalcRequestSchema(BaseModel):
	cart_value: int = Field(ge=0)
	delivery_distance: int
	number_of_items: int = Field(ge=1)
	time: customTime



try:
    FeeCalcRequestSchema(cart_value=2, delivery_distance=2,number_of_items=1, time='9999-04-23T13:00:00Z' )
except ValidationError as e:
    print(e)

