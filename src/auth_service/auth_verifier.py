import logging
import threading
from typing import Dict, Any, List
from src.db import DB
from src.models import Condition
from src.utils import is_param_valid

ATTRIBUTE_TYPES = ["string", "integer", "boolean"]
OPERATORS = ["=", "<", ">", "starts_with"]


class AuthVerifier:
    def __init__(self, user_id: str, resource_id: str, db=None):
        self.db = db or DB()
        self.user_id = user_id
        self.resource_id = resource_id

        self.user_attributes: Dict[str, Any] = dict()
        self.resource_policies: List[str] = list()

        self.is_authorized = False

    def init(self):
        if not is_param_valid(self.user_id, str) or not is_param_valid(self.resource_id, str):
            raise Exception("Got unexpected parameter type")

        self.user_attributes = self.db.get_user(self.user_id)
        self.resource_policies = self.db.get_resource_policies(self.resource_id)

    def verify(self):
        threads = []
        for policy_id in self.resource_policies:
            thread = threading.Thread(target=self.is_policy_fulfilled, args=policy_id)
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return self.is_authorized

    def is_policy_fulfilled(self, policy_id: str) -> None:
        conditions = self.db.get_policy_condition(policy_id)
        if len(conditions) > len(self.user_attributes):
            return
        for condition in conditions:
            condition_obj = Condition.from_dict(condition)
            if ((condition_obj.attribute_name not in self.user_attributes or
                 not self.is_condition_met(condition_obj, self.user_attributes[condition_obj.attribute_name])) or
                    self.is_authorized):
                return

        self.is_authorized = True

    # Checking condition_value operator user_value is met
    # For example       5         <         7
    @staticmethod
    def is_condition_met(condition_obj: Condition, user_val: Any) -> bool:
        try:
            if condition_obj.operator == "=":
                return condition_obj.value == user_val
            elif condition_obj.operator == "<":
                return condition_obj.value < user_val
            elif condition_obj.operator == ">":
                return condition_obj.value > user_val
            elif condition_obj.operator == "starts_with":
                return user_val.startswith(condition_obj.value)
            else:
                # Shouldn't happen
                raise Exception(f"Got unexpected operator: {condition_obj.operator}")
        except Exception:
            logging.exception("Failed to run condition validation")
        return False
