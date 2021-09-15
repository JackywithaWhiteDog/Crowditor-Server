"""Overview endpoints for the application.

This module contains the endpoint for the overview.

    Typical usage example:

    from app import api, docs
    from app.views.overview import OverviewAPI

    api.add_resource(OverviewAPI, '/overview')
    docs.register(OverviewAPI)

"""
import pathlib
import pickle

from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import Schema, fields

from app.utils.schema import WordcloudField, LineChartField, StackedBarChartField, TableField

FILE_PATH = pathlib.Path(__file__).parent.resolve()

with open(FILE_PATH / '../data/preprocessed/overview.pickle', 'rb') as file:
    data = pickle.load(file)


class OverviewResponseSchema(Schema):
    """Schema for the response to the overview endpoint."""
    keywords = fields.Dict(keys=fields.Str(), values=WordcloudField)
    helpful_tokens = WordcloudField
    success_rate = LineChartField
    achievement_rate = LineChartField
    funds = LineChartField
    domain_cnt = StackedBarChartField
    domain_success_rate = StackedBarChartField
    funds_ranking = TableField
    achievement_rate_ranking = TableField
    success_rate_6_mon = fields.Float()


class OverviewAPI(MethodResource, Resource):
    """Overview aendpoint."""

    @doc(description='Overview', tags=['Overview'])
    @marshal_with(OverviewResponseSchema)
    def get(self) -> dict:
        """Get the overview.

        Accepts GET request and return a 200 OK response
        with overview in JSON body.

        """
        return data
