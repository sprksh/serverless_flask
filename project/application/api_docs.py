import inspect
import yaml

import marshmallow
from apispec import APISpec

# from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from flasgger import Swagger

from project.api import serializers
from project.api.v1.scheme_apis import get_scheme, get_schemes


def setup_schema_definition(spec):
    for name, obj in inspect.getmembers(serializers):
        if inspect.isclass(obj) and type(obj) == marshmallow.schema.SchemaMeta:
            try:
                spec.components.schema(name, schema=obj)
            except Exception as e:
                pass


OPENAPI_SPEC = """
openapi: 3.0.2
info:
    description: |
        This is the admin server.
        For this sample, you can use the auth token `some-special-token` to test the authorization filters.
        # Introduction
        This API is documented in **OpenAPI format**.
    contact:
        name: API Support
        email: sprksh.j@gmail.com
        url: http://10.40.6.228
    x-logo:
        url: 'https://redocly.github.io/redoc/petstore-logo.png'
        altText: Project logo
    termsOfService: 'http://swagger.io/terms/'
servers:
- url: http://10.40.6.228
  description: Staging server (uses live data)
- url: http://10.40.6.228
  description: Dev server (uses test data)
components:
    securitySchemes:
        Authorization:
            description: A header named `Authorization` containing the bearer token in the format `Bearer <token>`
            type: http
            scheme: bearer
"""


def setup_path(spec):
    # define paths

    # scheme data
    spec.path(view=get_scheme)
    spec.path(view=get_schemes)


def init_docs(app):
    ctx = app.test_request_context()
    ctx.push()
    settings = yaml.safe_load(OPENAPI_SPEC)

    # Create an APISpec
    spec = APISpec(
        title="Swagger Project",
        version="1.0.0",
        openapi_version="3.0.2",
        plugins=[FlaskPlugin()],
        **settings
    )
    setup_schema_definition(spec)
    setup_path(spec)
    with open("project/docs/swagger.yml", "w") as swagger_file:
        swagger_file.write(spec.to_yaml())
    app.config["SWAGGER"] = {"title": "Swagger Project", "openapi": "3.0.2"}
    Swagger(app, template=spec.to_dict())
