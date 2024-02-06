import logging
from gevent import pywsgi

from flask import Flask, request, jsonify, Response
from http import HTTPStatus

from src.auth_service.auth_verifier import AuthVerifier

app = Flask(__name__)
LOG = logging.getLogger(__name__)


@app.route('/is_authorized', methods=['GET'])
def is_authorized():
    try:
        auth_service = AuthVerifier(request.json.get('user_id'), request.json.get('resource_id'))
        auth_service.init()
        decision = auth_service.verify()

        return jsonify(decision)
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
