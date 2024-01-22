import inspect
from math import ceil
from datetime import  datetime


class FeeCalculator:
    def __init__(self, config):
        self.config = config
    def surcharge_base(self, cart_value) -> int:
        surcharge = max(self.config.get("min_cart_value") - cart_value, 0)
        return (surcharge)
    def surcharge_distance(self, delivery_distance) -> int:
        gradient_distance = ceil(max(delivery_distance - self.config.get("base_delivery_distance"), 0)/self.config.get("gradient_distance"))
        surcharge = gradient_distance * self.config.get("gradient_price_distance_value") + self.config.get("base_delivery_distance_value")
        return (surcharge)
    def surcharge_numb_of_items(self, number_of_items: int) -> int:
        surcharge_1 = max(number_of_items - self.config.get("base_number_of_items") , 0)*self.config.get("gradient_price_per_extra_item")
        surcharge_2 = 0 if number_of_items < 12  else self.config.get("large_number_of_items_penalty_value") 
        surcharge = surcharge_1 +  surcharge_2
        return (surcharge)
    def surcharge_rush_hours(self, order_time: datetime, total_surcharge: int) -> int:
        order_time = datetime.strptime(order_time, '%Y-%m-%dT%H:%M:%SZ')
        if order_time.weekday() in self.config.get("rush_hour_days"):
            if order_time.hour >= self.config.get("rush_hour_start_hour") and order_time.hour <= self.config.get("rush_hour_end_hour"):
                total_surcharge = self.config.get("rush_hour_multiplier")*total_surcharge
        return (total_surcharge)
    def fee_cap(self, total_surcharge) -> int:
        delivery_fee = min(self.config.get("max_delivery_fee_value"), total_surcharge)
        return (delivery_fee)
    




def calculate_fee(input, config):
    input = input.dict()
    print(type(config))
    if input.get("cart_value") > config.get("free_delivery_eligible_cart_value"):
        capped_surcharge = 0
    else:
        feeCalculator = FeeCalculator(config)
        surcharge_base = feeCalculator.surcharge_base(input.get("cart_value"))
        surcharge_distance = feeCalculator.surcharge_distance(input.get("delivery_distance"))
        surcharge_numb_of_items = feeCalculator.surcharge_numb_of_items(input.get("number_of_items"))
        total_surcharge = surcharge_base + surcharge_distance + surcharge_numb_of_items
        total_surcharge_rushhour = feeCalculator.surcharge_rush_hours(order_time=input.get("time"), total_surcharge=total_surcharge)
        capped_surcharge = feeCalculator.fee_cap(total_surcharge_rushhour)
    return (capped_surcharge)




"""
class deliveryFeeCalculator(Calculator):
    def __init__(self, config):
        super().__init__(config)
    def add_all(cart_value: int, delivery_distance: int):
        #calculator = Calculator(db)
        surcharge_base = surcharge_base(cart_value)
        surcharge_distance = surcharge_distance(delivery_distance)
        total_surcharge = surcharge_base + surcharge_distance
        capped_surcharge = fee_cap(total_surcharge)
        return (capped_surcharge)
"""

