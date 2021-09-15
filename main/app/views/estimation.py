"""Estimation endpoints for the application.

This module contains the endpoint for the estimation.

    Typical usage example:

    from app import api, docs
    from app.views.estimation import EstimationAPI

    api.add_resource(EstimationAPI, '/estimation')
    docs.register(EstimationAPI)

"""
import pathlib
import pickle

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from app.utils.schema import (ProjectSchema, TableField, CateField,
    MetadataField, StackedBarChartField)
from app.utils.estimate import get_estimation

FILE_PATH = pathlib.Path(__file__).parent.resolve()

with open(FILE_PATH / '../data/preprocessed/success_rates_by_score.pickle', 'rb') as file:
    success_rates_by_score = pickle.load(file)

EstimationRequestSchema = ProjectSchema

class EstimationResponseSchema(Schema):
    """Schema for the response to the estimation endpoint."""
    success_rates_by_score = StackedBarChartField
    score = fields.Float()
    greater_than = fields.Float()
    peer_cnt = fields.Int()
    peer_success_cnt = fields.Int()
    peers = TableField
    categories = fields.Dict(key=fields.Str(), values=CateField)
    recommend_tokens = fields.Dict(key=fields.Str(), values=TableField)
    metadata = fields.Dict(keys=fields.Str(), values=MetadataField)

class EstimationAPI(MethodResource, Resource):
    """Estimation aendpoint."""

    @doc(description='Estimation', tags=['Estimation'])
    @use_kwargs(EstimationRequestSchema, location=('json'))
    @marshal_with(EstimationResponseSchema)
    def post(self, **kwargs) -> dict:
        """Post for the estimation.

        Accepts POST request and return a 200 OK response
        with estimation in JSON body.

        """
        return {
            **success_rates_by_score,
            **get_estimation(kwargs)
        }
