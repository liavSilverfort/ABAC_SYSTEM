import logging
from gevent import pywsgi

from flask import Flask, request, jsonify, Response
from http import HTTPStatus

from src.data_syncer_service.http_server import HttpServer

app = Flask(__name__)
LOG = logging.getLogger(__name__)

http_server = HttpServer()


@app.route('/attributes', methods=['POST'])
def create_attr():
    try:
        http_server.create_attr(request.json.get('attribute_name'), request.json.get('attribute_type'))
    except Exception:
        LOG.exception("Exception occurred while creating attribute")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/users', methods=['POST'])
def create_user():
    try:
        http_server.create_user(request.json.get('user_id'), request.json.get('attributes'))
    except Exception:
        LOG.exception("Exception occurred while creating user")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/policies', methods=['POST'])
def create_policy():
    try:
        http_server.create_policy(request.json.get('policy_id'), request.json.get('conditions'))
    except Exception:
        LOG.exception("Exception occurred while creating policy")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/policies/<policy_id>', methods=['PUT'])
def update_policy(policy_id):
    try:
        http_server.update_policy(policy_id, request.json.get('conditions'))
    except Exception:
        LOG.exception("Exception occurred while updating policy")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/resources', methods=['POST'])
def create_resource():
    try:
        http_server.create_resource(request.json.get('resource_id'), request.json.get('policy_ids'))
    except Exception:
        LOG.exception("Exception occurred while creating resource")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/resources/<resource_id>', methods=['PUT'])
def update_resource(resource_id):
    try:
        http_server.update_resource(resource_id, request.json.get('policy_ids'))
    except Exception:
        LOG.exception("Exception occurred while updating resource")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return Response(status=HTTPStatus.OK)


@app.route('/is_authorized', methods=['GET'])
def is_authorized():
    try:
        return jsonify(http_server.is_authorized(request.json.get('user_id'), request.json.get('resource_id')))
    except Exception:
        LOG.exception("Exception occurred while calling is_authorized")
        return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)


def create_server():
    server = pywsgi.WSGIServer(('', 80), app)
    return server


application = app


def main():
    LOG.info("Server starting...")
    print("Server starting...")
    server = create_server()
    server.serve_forever()
    LOG.info("Server finished")


if __name__ == '__main__':
    main()
