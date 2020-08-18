import logging
from flask import Flask, request, Blueprint

logger = logging.getLogger(__name__)

project_bp = Blueprint("project_flask", __name__, url_prefix="/project/")


@project_bp.route("/ping/")
def hello():
    result = {"statusCode": 200, "data": "Pong"}
    return result

