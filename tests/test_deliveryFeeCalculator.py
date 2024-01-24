import os
import json
import pytest
import sys
sys.path.append('./src/')
from tools import deliveryFeeCalculator
from tools.loadDb import load_db

# future time?

cases_1 = [
    {"data" :{"cart_value":890, "delivery_distance":30, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 110},
    {"data" :{"cart_value":120, "delivery_distance":3, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 880},
    {"data" :{"cart_value":1200, "delivery_distance":3, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 0}
]

cases_2 = [
    {"data" :{"cart_value":890, "delivery_distance":1000, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 200},
    {"data" :{"cart_value":120, "delivery_distance":1499, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 300},
    {"data" :{"cart_value":1200, "delivery_distance":1501, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 400}
]

cases_3 = [
    {"data" :{"cart_value":890, "delivery_distance":1000, "number_of_items":4, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 0},
    {"data" :{"cart_value":120, "delivery_distance":1000, "number_of_items":5, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 50},
    {"data" :{"cart_value":1200, "delivery_distance":1000, "number_of_items":10, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 300},
    {"data" :{"cart_value":890, "delivery_distance":1000, "number_of_items":13, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 570},
    {"data" :{"cart_value":120, "delivery_distance":1000, "number_of_items":14, "time": "2024-05-22T12:23:04Z"}, "expected_surcharge": 620}
]

cases_4 = [
    {"data" :{"cart_value":890, "delivery_distance":1501, "number_of_items":4, "time": "2024-01-05T12:23:04Z", "total_surcharge_before_rush" : 510}, "expected_total_surcharge": 510},
    {"data" :{"cart_value":120, "delivery_distance":1000, "number_of_items":5, "time": "2024-01-05T15:23:04Z", "total_surcharge_before_rush" : 1130}, "expected_total_surcharge": 1356},
    {"data" :{"cart_value":1200, "delivery_distance":1501, "number_of_items":10, "time": "2024-01-05T16:23:04Z", "total_surcharge_before_rush" : 700}, "expected_total_surcharge": 840},
    {"data" :{"cart_value":890, "delivery_distance":1499, "number_of_items":13, "time": "2024-01-05T19:23:04Z", "total_surcharge_before_rush" : 980}, "expected_total_surcharge": 980},
    {"data" :{"cart_value":120, "delivery_distance":1000, "number_of_items":14, "time": "2024-01-06T15:23:04Z", "total_surcharge_before_rush" : 1700}, "expected_total_surcharge": 1700}
]

cases_5 = [
    {"data" :{ "total_surcharge" : 1499}, "expected_capped_surcharge": 1499},
    {"data" :{ "total_surcharge" : 1500}, "expected_capped_surcharge": 1500},
    {"data" :{ "total_surcharge" : 1501}, "expected_capped_surcharge": 1500}
]

@pytest.fixture(scope="module", autouse=True)
def mock__feeCalculatorObj():
    db = load_db()
    feeCalculator = deliveryFeeCalculator.FeeCalculator(db)
    return feeCalculator

@pytest.mark.parametrize("min_cart_value_cases", cases_1)
def test_surcharge_base_cases(min_cart_value_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    cart_value = min_cart_value_cases.get("data").get("cart_value")
    expected_surcharge = min_cart_value_cases.get("expected_surcharge")
    assert feeCalculator.surcharge_base(cart_value) == expected_surcharge


@pytest.mark.parametrize("distance_cases", cases_2)
def test_surcharge_distance(distance_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    delivery_distance = distance_cases.get("data").get("delivery_distance")
    expected_surcharge = distance_cases.get("expected_surcharge")
    assert feeCalculator.surcharge_distance(delivery_distance) == expected_surcharge

# surcharge_numb_of_items
@pytest.mark.parametrize("num_of_item_cases", cases_3)
def test_surcharge_numb_of_items(num_of_item_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    num_of_item = num_of_item_cases.get("data").get("number_of_items")
    expected_surcharge = num_of_item_cases.get("expected_surcharge")
    assert feeCalculator.surcharge_numb_of_items(num_of_item) == expected_surcharge

# surcharge_rush_hours
@pytest.mark.parametrize("rush_hours_cases", cases_4)
def test_surcharge_rush_hours(rush_hours_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    order_time = rush_hours_cases.get("data").get("time")
    total_surcharge_before_rush = rush_hours_cases.get("data").get("total_surcharge_before_rush")
    expected_total_surcharge = rush_hours_cases.get("expected_total_surcharge")
    assert feeCalculator.surcharge_rush_hours(order_time, total_surcharge_before_rush) == expected_total_surcharge 

# fee_cap
@pytest.mark.parametrize("fee_cap_cases", cases_5)
def test_fee_cap(fee_cap_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    total_surcharge = fee_cap_cases.get("data").get("total_surcharge")
    expected_capped_surcharge = fee_cap_cases.get("expected_capped_surcharge")
    assert feeCalculator.fee_cap(total_surcharge) == expected_capped_surcharge 

# free_delivery