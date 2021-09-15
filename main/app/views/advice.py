"""Advice endpoints for the application.

This module contains the endpoint for the advice.

    Typical usage example:

    from app import api, docs
    from app.views.advice import AdviceAPI

    api.add_resource(AdviceAPI, '/advice')
    docs.register(AdviceAPI)

"""
import pathlib
import pickle

from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from app.utils.schema import AdviceField

FILE_PATH = pathlib.Path(__file__).parent.resolve()

with open(FILE_PATH / '../data/preprocessed/advice.pickle', 'rb') as file:
    data = pickle.load(file)

class AdviceResponseSchema(Schema):
    """Schema for the response to the advice endpoint."""
    data = fields.Dict(keys=fields.Str, values=AdviceField)

class AdviceAPI(MethodResource, Resource):
    """Advice aendpoint."""

    @doc(description='Advice', tags=['Advice'])
    @marshal_with(AdviceResponseSchema)
    def get(self) -> dict:
        """Get for the advice.

        Accepts GET request and return a 200 OK response
        with advice in JSON body.

        """
        return data
