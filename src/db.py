import json
from typing import Dict, Any
import redis
import logging

ATTR_PREFIX = "attr_"
POLICY_PREFIX = "policy_"
RESOURCE_PREFIX = "resource_"
USER_PREFIX = "user_"


class DB:
    def __init__(self):
        self.redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, db=0)

    def attr_exists(self, key: str) -> bool:
        return self._exists(ATTR_PREFIX + key)

    def user_exists(self, key: str) -> bool:
        return self._exists(USER_PREFIX + key)

    def resource_exists(self, key: str) -> bool:
        return self._exists(RESOURCE_PREFIX + key)

    def policy_exists(self, key: str) -> bool:
        return self._exists(POLICY_PREFIX + key)

    def _exists(self, key: str):
        return self.redis_client.exists(key)

    def set_attribute(self, attribute_name: str, attribute_type: str):
        self.redis_client.set(ATTR_PREFIX + attribute_name, attribute_type)
        logging.info(f"A new attribute was created: {attribute_name}")

    def get_attr(self, attribute_name: str):
        return self.redis_client.get(attribute_name)

    def set_user(self, user_id: str, attributes: Dict[str, Any]):
        self.redis_client.hset(USER_PREFIX + user_id, mapping=attributes)
        logging.info(f"A new user was created: {user_id}")

    def get_user(self, user_id: str):
        self.redis_client.hgetall(USER_PREFIX + user_id)

    def set_policy(self, policy_id: str, conditions: list[Dict[str, Any]]):
        self.redis_client.set(POLICY_PREFIX + policy_id, json.dumps(conditions))

    def get_policy_condition(self, policy_id: str):
        return json.loads(self.redis_client.get(POLICY_PREFIX + policy_id))

    def set_resource(self, resource_id: str, policy_ids: list[str]):
        self.redis_client.set(RESOURCE_PREFIX + resource_id, json.dumps(policy_ids))
        logging.info(f"A new resource was created: {resource_id}")

    def get_resource_policies(self, resource_id: str):
        return json.loads(self.redis_client.get(RESOURCE_PREFIX + resource_id))
