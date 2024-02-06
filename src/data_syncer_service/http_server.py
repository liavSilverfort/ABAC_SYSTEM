import logging
from typing import Dict, Any

from src.utils import is_param_valid
from src.db import DB
from src.models import Condition

ATTRIBUTE_TYPES = ["string", "integer", "boolean"]
OPERATORS = ["=", "<", ">", "starts_with"]


class HttpServer:
    def __init__(self, db: DB = None):
        self.db = db or DB()

    def create_attr(self, attribute_name: str, attribute_type: str):
        if not is_param_valid(attribute_name, str) or not is_param_valid(attribute_type, str):
            raise Exception("Got unexpected parameter type")
        if not self.db.attr_exists(attribute_name) and attribute_type in ATTRIBUTE_TYPES:
            self.db.set_attribute(attribute_name, attribute_type)
        else:
            raise Exception("Attr already exists or got unexpected type")

    def create_user(self, user_id: str, attributes: Dict[str, Any]):
        if not is_param_valid(user_id, str) or not is_param_valid(attributes, dict):
            raise Exception("Got unexpected parameter type")

        if not self.db.user_exists(user_id):
            for attribute_name, attribute_value in attributes.items():
                if not self.is_attribute_valid(attribute_name, attribute_value):
                    raise Exception(f"{attribute_name} attribute doesn't exist or the attribute type is invalid")
            self.db.set_user(user_id, attributes)
        else:
            raise Exception("User already exists")

    def create_policy(self, policy_id: str, conditions: list[Dict[str, Any]]):
        if not is_param_valid(policy_id, str) or not is_param_valid(conditions, list):
            raise Exception("Got unexpected parameter type")

        if not self.db.policy_exists(policy_id):
            if not self.are_conditions_valid(conditions):
                raise Exception(f"Got invalid condition/s: {conditions}")
            self.db.set_policy(policy_id, conditions)
            logging.info(f"A new policy was created: {policy_id}")
        else:
            raise Exception("Policy already exists")

    def update_policy(self, policy_id: str, conditions: list[Dict[str, Any]]):
        if not is_param_valid(policy_id, str) or not is_param_valid(conditions, list):
            raise Exception("Got unexpected parameter type")

        if self.db.policy_exists(policy_id):
            if not self.are_conditions_valid(conditions):
                raise Exception(f"Got invalid condition/s: {conditions}")
            self.db.set_policy(policy_id, conditions)
        else:
            raise Exception("Policy doesn't exists")

    def create_resource(self, resource_id: str, policy_ids: list[str]):
        if not is_param_valid(resource_id, str) or not is_param_valid(policy_ids, list):
            raise Exception("Got unexpected parameter type")

        if not self.db.resource_exists(resource_id):
            for policy_id in policy_ids:
                if not self.db.policy_exists(policy_id):
                    raise Exception(f"Policy {policy_id} doesn't exist")
            self.db.set_resource(resource_id, policy_ids)
            logging.info(f"A new resource was created: {resource_id}")
        else:
            raise Exception("Resource already exists")

    def update_resource(self, resource_id: str, policy_ids: list[str]):
        if not is_param_valid(resource_id, str) or not is_param_valid(policy_ids, list):
            raise Exception("Got unexpected parameter type")

        if self.db.resource_exists(resource_id):
            for policy_id in policy_ids:
                if not self.db.policy_exists(policy_id):
                    raise Exception(f"Policy {policy_id} doesn't exist")
            self.db.set_resource(resource_id, policy_ids)
        else:
            raise Exception("Resource doesn't exists")

    def is_attribute_valid(self, attribute_name: str, attribute_value: Any):
        if not self.db.attr_exists(attribute_name):
            return False
        attribute_type = self.db.get_attr(attribute_name)
        if attribute_type == "boolean":
            return isinstance(attribute_value, bool)
        elif attribute_type == "string":
            return isinstance(attribute_value, str)
        elif attribute_type == "integer":
            return isinstance(attribute_value, int)
        return False

    def are_conditions_valid(self, conditions: list[Dict[str, Any]]):
        for condition in conditions:
            condition_obj = Condition.from_dict(condition)
            if condition_obj.operator not in OPERATORS or not self.is_attribute_valid(condition_obj.attribute_name,
                                                                                      condition_obj.value):
                return False
