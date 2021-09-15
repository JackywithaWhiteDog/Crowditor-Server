"""Basic schema for the request / response

This module collects some basic schemas for the application

    Typical usage example:

    from app.utils.schema import [SCHEMA_NAME]

"""
from marshmallow import Schema, fields

class MessageSchema(Schema):
    """Basic schema for message

    Attributes:
        message (str): message to response

    """
    message = fields.Str()


class ProjectInfoSchema(Schema):
    """Basic schema for project info

    Attributes:
        title (str): Project title
        id (int): Project ID

    """

    title = fields.Str(required=True)
    id = fields.Int(required=True)


class ProjectSchema(Schema):
    """Basic schema for project

    Attributes:
        title (str): Project title
        description (str): Project description
        content (str): Project content
        goal (int): Target goal
        type (str): Project type (e.g., 群眾集資、預購式專案)
        domain (str): Project domain (e.g., 科技、設計、社會)
        start_time (datetime): Project start time
                               (ISO8601 format: 2014-12-22T03:12:58.019077+00:00)
        end_time (datetime): Project end time
        website (bool): True if the project has a website
        facebook (bool): True if the project has a facebook page
        instagram (bool): True if the project has an instagram page
        youtube (bool): True if the project has a youtube page
        set_count (int): Number of sets
        max_set_prices (int): Maximum set price
        min_set_prices (int): Minimum set price

    """

    title = fields.Str(required=True)
    description = fields.Str(required=True)
    content = fields.Str(required=True)
    goal = fields.Int(required=True)
    type = fields.Str(required=True)
    domain = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    website = fields.Bool(required=True)
    facebook = fields.Bool(required=True)
    instagram = fields.Bool(required=True)
    youtube = fields.Bool(required=True)
    set_count = fields.Int(required=True)
    max_set_prices = fields.Int(required=True)
    min_set_prices = fields.Int(required=True)


class WordcloudTokenSchema(Schema):
    """Basic schema for single token of wordcloud

    Attributes:
        text (str): Token text
        value (float): Weight of token (the higher the larger)

    """
    text = fields.Str()
    value = fields.Float()


WordcloudField = fields.List(fields.Nested(WordcloudTokenSchema))


class LineChartSchema(Schema):
    """Basic schema for line chart

    Attributes:
        labels (list[Any]): list of labels
        items (list[float]): list of nodes

    """
    labels = fields.List(fields.Raw())
    items = fields.List(fields.Float())


LineChartField = fields.Nested(LineChartSchema)


class StackedBarChartItemSchema(Schema):
    """Basic schema for item of stacked bar chart

    Attributes:
        name (str): name of item
        data (list[float]): list of data point

    """
    name = fields.Str()
    data = fields.List(fields.Float())


class StackedBarChartSchema(Schema):
    """Basic schema for line chart

    Attributes:
        labels (list[Any]): list of labels
        items (list[float]): list of items

    """
    labels = fields.List(fields.Raw())
    items = fields.List(fields.Nested(StackedBarChartItemSchema))


StackedBarChartField = fields.Nested(StackedBarChartSchema)

TableField = fields.List(fields.Dict(keys=fields.Str(), values=fields.Raw()))

class AdviceSchema(Schema):
    """Basic schema for advice

    Attributes:
        total_cnt (int)
        keywords (Table): tokens with highest document frequency
        success_rate (float)
        goal (int)
        duration_days (int)
        description_length (int)
        content_length (int)

    """
    total_cnt = fields.Int()
    keywords = TableField
    success_rate = fields.Float()
    goal = fields.Int()
    duration_days = fields.Int()
    description_length = fields.Int()
    content_length = fields.Int()

AdviceField = fields.Nested(AdviceSchema)

class CateItemSchema(Schema):
    """Basic schema for category item

    Attributes:
        name (str): Category name
        rate (float): Category frequency

    """
    name = fields.Str()
    rate = fields.Float()

class CateSchema(Schema):
    """Basic schema for category

    Attributes:
        same_rate (float): rate for same category
        most (CateItem)

    """
    same_rate = fields.Float()
    most = fields.Nested(CateItemSchema)

CateField = fields.Nested(CateSchema)

class MetadataSchema(Schema):
    """Basic schema for metadata

    Attributes:
        box_min (float)
        box_25 (float)
        box_50 (float)
        box_75 (float)
        box_max (float)
        success_median (float)
        failure_median (float)
        success_greater (int)
        success_less (int)
        project_value (float)

    """
    box_min = fields.Float()
    box_25 = fields.Float()
    box_50 = fields.Float()
    box_75 = fields.Float()
    box_max = fields.Float()
    success_median = fields.Float()
    failure_median = fields.Float()
    success_greater = fields.Int()
    success_less = fields.Int()
    project_value = fields.Float()

MetadataField = fields.Nested(MetadataSchema)
