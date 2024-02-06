import pytest

from src.auth_service.auth_verifier import AuthVerifier
from unittest.mock import MagicMock

from src.models import Condition


@pytest.fixture
def condition_in_dict():
    return {"attribute_name": "attr_1", "operator": "=", "value": 5}


@pytest.fixture
def conditions():
    return [
        {"attribute_name": "attr_1", "operator": "=", "value": "5"},
        {"attribute_name": "attr_2", "operator": "<", "value": 4},
        {"attribute_name": "attr_3", "operator": ">", "value": 2},
        {"attribute_name": "attr_4", "operator": "starts_with", "value": "pre"},
    ]


@pytest.fixture
def user_attributes():
    return ({
        "attr_1": "5",
        "attr_2": 6,
        "attr_3": 1,
        "attr_4": "prepre",
    })


@pytest.fixture
def user_id():
    return "user_1"


@pytest.fixture
def resource_id():
    return "resource_1"


@pytest.fixture
def policy_id():
    return "policy_1"


@pytest.fixture
def auth_verifier(user_id, resource_id):
    return AuthVerifier(user_id, resource_id, MagicMock())


def test_is_policy_fulfilled(auth_verifier, conditions, user_attributes, policy_id):
    # Test 1
    auth_verifier.is_authorized = False
    auth_verifier.db.get_policy_condition = MagicMock(return_value=conditions)
    auth_verifier.user_attributes = user_attributes
    auth_verifier.is_policy_fulfilled(policy_id)
    assert auth_verifier.is_authorized

    # Test 2
    auth_verifier.is_authorized = False
    auth_verifier.user_attributes["attr_1"] = "6"
    auth_verifier.is_policy_fulfilled(policy_id)
    assert not auth_verifier.is_authorized


def test_is_condition_met(auth_verifier, condition_in_dict):
    condition = Condition.from_dict(condition_in_dict)
    assert auth_verifier.is_condition_met(condition, 5)
