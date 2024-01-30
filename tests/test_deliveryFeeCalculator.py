import pytest
import sys
sys.path.append('./src/')
from tools import deliveryFeeCalculator  # noqa: E402
from tools.loadDb import load_db  # noqa: E402


# min_cart_value_cases
cases_1 = [
    {"data": {"cart_value": 890}, "expected_surcharge": 110},
    {"data": {"cart_value": 120}, "expected_surcharge": 880},
    {"data": {"cart_value": 1200}, "expected_surcharge": 0}
]

# distance_cases
cases_2 = [
    {"data": {"delivery_distance": 1000}, "expected_surcharge": 200},
    {"data": {"delivery_distance": 1499}, "expected_surcharge": 300},
    {"data": {"delivery_distance": 1501}, "expected_surcharge": 400}
]

# num_of_item_cases
cases_3 = [
    {"data": {"number_of_items": 4}, "expected_surcharge": 0},
    {"data": {"number_of_items": 5}, "expected_surcharge": 50},
    {"data": {"number_of_items": 10}, "expected_surcharge": 300},
    {"data": {"number_of_items": 13}, "expected_surcharge": 570},
    {"data": {"number_of_items": 14}, "expected_surcharge": 620}
]

# rush_hours_cases
cases_4 = [
    {"data": {"time": "2024-01-05T12:23:04Z", "total_surcharge_before_rush": 510},
     "expected_total_surcharge": 510},
    {"data": {"time": "2024-01-05T15:23:04Z", "total_surcharge_before_rush": 1130},
     "expected_total_surcharge": 1356},
    {"data": {"time": "2024-01-05T16:23:04Z", "total_surcharge_before_rush": 700},
     "expected_total_surcharge": 840},
    {"data": {"time": "2024-01-05T19:23:04Z", "total_surcharge_before_rush": 980},
     "expected_total_surcharge": 980},
    {"data": {"time": "2024-01-06T15:23:04Z", "total_surcharge_before_rush": 1700},
     "expected_total_surcharge": 1700}
]

# fee_cap_cases
cases_5 = [
    {"data": {"total_surcharge": 1499}, "expected_capped_surcharge": 1499},
    {"data": {"total_surcharge": 1500}, "expected_capped_surcharge": 1500},
    {"data": {"total_surcharge": 1501}, "expected_capped_surcharge": 1500}
]

# free_delivery cases
cases_6 = [
    {"data": {"cart_value": 20000}, "is_free_delivery": True},
    {"data": {"cart_value": 19999}, "is_free_delivery": False},
    {"data": {"cart_value": 30000}, "is_free_delivery": True}
]

# total cost cases
cases_7 = [
    {"data": {"cart_value": 790, "delivery_distance": 2235,
              "number_of_items": 4, "time": "2024-01-15T13:00:00Z"},
     "delivery_fee": 710},
    {"data": {"cart_value": 890, "delivery_distance": 1501,
              "number_of_items": 4, "time": "2024-01-05T12:23:04Z"},
     "delivery_fee": 510},
    {"data": {"cart_value": 30000, "delivery_distance": 1501,
              "number_of_items": 4, "time": "2024-01-05T12:23:04Z"},
     "delivery_fee": 0},
]


@pytest.fixture(scope="module", autouse=True)
def mock__feeCalculatorObj():
    db = load_db()
    feeCalculator = deliveryFeeCalculator.FeeCalculator(db)
    return feeCalculator


@pytest.fixture(scope="module", autouse=True)
def mock__db():
    db = load_db()
    return db


# min_cart_value_cases
@pytest.mark.parametrize("min_cart_value_cases", cases_1)
def test_surcharge_base_cases(min_cart_value_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    cart_value = min_cart_value_cases.get("data").get("cart_value")
    expected_surcharge = min_cart_value_cases.get("expected_surcharge")
    assert feeCalculator.surcharge_base(cart_value) == expected_surcharge


# distance_cases
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


# fee_cap_cases
@pytest.mark.parametrize("fee_cap_cases", cases_5)
def test_fee_cap(fee_cap_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    total_surcharge = fee_cap_cases.get("data").get("total_surcharge")
    expected_capped_surcharge = fee_cap_cases.get("expected_capped_surcharge")
    assert feeCalculator.fee_cap(total_surcharge) == expected_capped_surcharge


# free_delivery
@pytest.mark.parametrize("free_delivery_cases", cases_6)
def test_is_free_delivery(free_delivery_cases, mock__feeCalculatorObj):
    feeCalculator = mock__feeCalculatorObj
    cart_value = free_delivery_cases.get("data").get("cart_value")
    is_free_delivery = free_delivery_cases.get("is_free_delivery")
    assert feeCalculator.is_free_delivery(cart_value) == is_free_delivery


# total charge
@pytest.mark.parametrize("free_delivery_cases", cases_7)
def test_calculate_fee(free_delivery_cases, mock__db):
    db = mock__db
    delivery_fee = deliveryFeeCalculator.calculate_fee(free_delivery_cases.get("data"), db)
    assert delivery_fee == free_delivery_cases.get("delivery_fee")
