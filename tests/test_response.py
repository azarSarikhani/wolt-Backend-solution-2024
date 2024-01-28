import os
import json
import pytest
from src.app import app
from fastapi.testclient import TestClient




client = TestClient(app)

def test_validRequestResponseSchema():
    response = client.post("/delivery_fee", json = {"cart_value":790, "delivery_distance":2235, "number_of_items":4, "time": "2024-01-15T13:00:00Z"})
    assert response.status_code == 200
    assert response.json().get("delivery_fee") != None


def test_invaliCartValue():
    response = client.post("/delivery_fee", json = {"cart_value":0, "delivery_distance":2235, "number_of_items":4, "time": "2024-01-15T13:00:00Z"})
    assert response.status_code == 422


def test_invaliDeliveryDistance():
    response = client.post("/delivery_fee", json = {"cart_value":90, "delivery_distance":-1, "number_of_items":4, "time": "2024-01-15T13:00:00Z"})
    assert response.status_code == 422


def test_missingRequetBody():
    response = client.post("/delivery_fee", json = {"number_of_items":4, "time": "2024-01-15T13:00:00Z"})
    assert response.status_code == 422
