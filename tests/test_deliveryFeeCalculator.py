import os
import json
import pytest
from src.tools import deliveryFeeCalculator
from src.tools.loadDb import load_db



surcharge_base_cases = [
    {"data" :{"cart_value":890, "delivery_distance":30, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 110},
     {"data" :{"cart_value":120, "delivery_distance":3, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 880},
     {"data" :{"cart_value":1200, "delivery_distance":3, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 0}
]

surcharge_distance_cases = [
    {"data" :{"cart_value":0, "delivery_distance":3, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}, "fee": 123},
     {"data" :{"cart_value":0, "delivery_distance":3, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}, "fee": 123}
]

@pytest.fixture(scope="module", autouse=True)
def mock__feeCalculatorObj():
    db = load_db()
    feeCalculator = deliveryFeeCalculator.FeeCalculator(db)
    return feeCalculator

@pytest.mark.parametrize("surcharge_base_cases", surcharge_base_cases)
def test_surcharge_base_cases(surcharge_base_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    assert feeCalculator.surcharge_base(surcharge_base_cases.get("data").get("cart_value")) == surcharge_base_cases.get("expected_surcharge")


#@pytest.mark.parametrize("surcharge_base_cases", surcharge_distance_cases)
#def test_surcharge_distance(surcharge_distance_cases):
    pass