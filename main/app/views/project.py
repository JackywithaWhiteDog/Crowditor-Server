"""Project endpoints for the application.

This module contains the endpoint for the project.

    Typical usage example:

    from app import api, docs
    from app.views.project import ProjectAPI

    api.add_resource(ProjectAPI, '/projects/<int:project_id>')
    docs.register(ProjectAPI)

"""
from datetime import datetime
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from app.utils.schema import ProjectSchema, MessageSchema

mock_data = {
    "content": "string",
    "description": "string",
    "domain": "string",
    "end_time": datetime.now(),
    "facebook": True,
    "goal": 0,
    "instagram": True,
    "max_set_price": 0,
    "min_set_price": 0,
    "set_count": 0,
    "start_time": datetime.now(),
    "title": "string",
    "type": "string",
    "website": True,
    "youtube": True
}

class ProjectAPI(MethodResource, Resource):
    """Project aendpoint."""

    @doc(description='Project', tags=['Projects'])
    @marshal_with(ProjectSchema)
    def get(self, project_id) -> dict:
        """Post for the project.

        Accepts POST request and return a 200 OK response
        with project in JSON body.

        """
        return mock_data

    @doc(descriptioProjectResponseScheman='Project', tags=['Projects'])
    @use_kwargs(ProjectSchema)
    @marshal_with(MessageSchema)
    def put(self, project_id, **kwargs) -> dict:
        """Update the project.

        Accepts POST request and return a 200 OK response
        with project in JSON body.

        """
        return {'message': 'updated'}

    @doc(descriptioProjectResponseScheman='Project', tags=['Projects'])
    @marshal_with(MessageSchema)
    def delete(self, project_id) -> dict:
        """Update the project.

        Accepts POST request and return a 200 OK response
        with project in JSON body.

        """
        return {'message': 'deleted'}
