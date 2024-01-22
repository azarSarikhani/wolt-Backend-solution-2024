from pydantic import BaseModel
from typing import Literal, List
from pydantic import BaseModel, Field,ValidationError



class InitialConfig(BaseModel):
	min_cart_value: int
	base_delivery_distance: int
	base_delivery_distance_value: int
	gradient_distance: int
	gradient_price_distance_value: int 
	base_number_of_items: int
	gradient_price_per_extra_item: int
	large_number_of_items: int
	large_number_of_items_penalty_value: int
	max_delivery_fee_value: int
	free_delivery_eligible_cart_value: int
	rush_hour_multiplier: float
	rush_hour_days: List[Literal[0, 1, 2, 3, 4, 5, 6]] = Field(min_length=1)
	rush_hour_start_hour: int
	rush_hour_end_hour: int





