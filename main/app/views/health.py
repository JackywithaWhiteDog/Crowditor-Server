"""Health check endpoints for the application.

This module contains the endpoint for the health check,
which accepts GET requests at /health and returns a 200 OK
response with JSON body {'status', 'ok'}.

    Typical usage example:

    from app import api, docs
    from app.views.health import HealthAPI

    api.add_resource(HealthAPI, '/health')
    docs.register(HealthAPI)

"""
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

class HealthResponseSchema(Schema):
    """Schema for the response to the health check endpoint.

    Attributes:
        status (str): Status of the health check.

    """
    status = fields.Str()

class HealthAPI(MethodResource, Resource):
    """Health check endpoint.

    Attributes:
        response (Schema): Response schema

    """

    @doc(description='Health check', tags=['Health'])
    @marshal_with(HealthResponseSchema)
    def get(self) -> dict:
        """Get the health check status.

        Accepts GET request and return a 200 OK response
        with JSON body {'status', 'ok'}.

        """
        return {'status': 'ok'}
