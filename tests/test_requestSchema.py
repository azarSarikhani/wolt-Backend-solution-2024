import os
import json
import pytest
from src.tools import deliveryFeeCalculator

@pytest.fixture(scope="module", autouse=True)
def mock__request_body():
    request_dict = {"cart_value":0, "delivery_distance":3, "number_of_items":1, "time": "2024-05-22T12:23:04Z"}
    return request_dict