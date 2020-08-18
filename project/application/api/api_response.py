from flask import jsonify
from flask.helpers import make_response

from application.utils import make_jsonify_ready


class ApiResponse:
    @staticmethod
    def build(status_code, data=None, errors=None, meta=None, resource_version=None):
        if not meta:
            meta = dict()
        if not data:
            data = dict()
        if not errors:
            errors = list()
        response = dict(data=data, errors=errors, meta=meta)
        if resource_version:
            response["resource_version"] = resource_version
        response = make_jsonify_ready(response)
        return make_response(jsonify(response), status_code)
