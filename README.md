# Linx Security Home Task - ABAC System
---

### Setting up and Running   
>`DNS`


###  Rest API Examples
>>POST /attributes
> 
> curl -X POST http://localhost:80/attributes -H "Content-Type: application/json" -d '{"attribute_name": "foo_attr", "attribute_type": "integer"}'
    
>> POST /users
> 
> curl -X POST http://localhost:80/users -H "Content-Type: application/json" -d '{"user_id": "user_1", "attributes": {"foo_attr":5}}'

>> POST /policies
> 
> curl -X POST http://localhost:80/policies -H "Content-Type: application/json" -d '{"policy_id": "policy_1", "conditions": [{"attribute_name:":"foo_attr", "operator": "=", "value": 5}]}'

>> POST /policies
> 
> curl -X PUT http://localhost:80/policies/policy_1 -H "Content-Type: application/json" -d '{"conditions": [{"attribute_name:":"foo_attr", "operator": "=", "value": 5}]}'

> POST /resources
> 
> > curl -X POST http://localhost:80/resources -H "Content-Type: application/json" -d '{"resource_id": "resource_1", "policy_ids": ["policy_1"]}'

> PUT /resources
> 
> > curl -X PUT http://localhost:80/resources/resource_1 -H "Content-Type: application/json" -d '{"policy_ids": ["policy_1"]}'

> GET /is_authorized
> 
> > curl -X GET http://localhost:80/is_authorized -H "Content-Type: application/json" -d '{"user_id": "user_1", "resource_id": "resource_1"}'


