"""Project list endpoints for the application.

This module contains the endpoint for the project list.

    Typical usage example:

    from app import api, docs
    from app.views.project_list import ProjectListAPI

    api.add_resource(ProjectListAPI, '/projects')
    docs.register(ProjectListAPI)

"""
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from app.utils.schema import ProjectInfoSchema, ProjectSchema, MessageSchema

class ProjectListResponseSchema(Schema):
    """Schema for the response to the project list endpoint."""
    projects = fields.List(fields.Nested(ProjectInfoSchema))

class ProjectListAPI(MethodResource, Resource):
    """Project list aendpoint."""

    @doc(description='Project list', tags=['Projects'])
    @marshal_with(ProjectListResponseSchema)
    def get(self) -> dict:
        """Get the project list.

        Accepts GET request and return a 200 OK response
        with project list in JSON body.

        """
        return {'projects': []}

    @doc(description='Project list', tags=['Projects'])
    @use_kwargs(ProjectSchema)
    @marshal_with(MessageSchema)
    def post(self) -> dict:
        """Get the project list.

        Accepts GET request and return a 200 OK response
        with project list in JSON body.

        """
        return {'message': 'created'}
