"""Flask server for the main application.

This module is the Flask server for the main application.
It exposes the RESTful APIs for the frontend, and handles
the logic with other microservices.

The server also provides the swagger endpoint at /swagger/,
and the swagger UI at /swagger-ui/.

    Typical usage example:

    from app import app
    app.run()

"""
import logging
from logging.config import fileConfig
import pathlib

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request, jsonify, Response
from flask_apispec.extension import FlaskApiSpec
from flask_restful import Api
from werkzeug.exceptions import HTTPException

FILE_PATH = pathlib.Path(__file__).parent.resolve()

fileConfig(FILE_PATH / 'logging.ini')

logger = logging.getLogger()

app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Crowditor Main API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/',
})
api = Api(app)
docs = FlaskApiSpec(app)


@app.before_request
def handle_before_request() -> None:
    """Records the request path and method.

    Logs the request path and method before handling request.

    """
    log_head = f'{request.method} {request.path}'
    logger.debug('[%s] get request', log_head)


@app.after_request
def handle_after_request(response: Response) -> Response:
    """Records the response status.

    Logs the response status after handling request.

    Args:
        response: The response object.

    Returns:
        The response object.

    """
    log_head = f'{request.method} {request.path} - {response.status_code}'
    if 200 <= response.status_code <= 299:
        logger.debug('[%s] successfully handle request', log_head)
    elif 300 <= response.status_code <= 399:
        logger.debug('[%s] redirect request', log_head)
    elif 400 <= response.status_code <= 499:
        logger.info('[%s] failed to handle request (client errors)', log_head)
    else:  # pragma: no cover
        logger.warning(
            '[%s] failed to handle request (server errors)', log_head)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.errorhandler(Exception)
def handle_error(error: Exception) -> Response:
    """Generates response with error.

    Converts the non HTTP exceptions into 500 Internal
    Server Error and logs the errors.

    Args:
        error: The Exception.

    Returns:
        The error response.

    """
    if isinstance(error, HTTPException):
        code = error.code
        error_string = str(error)
    else:  # pragma: no cover
        log_head = f'{request.method} {request.path}'
        logger.warning('[%s] %s', log_head, str(error))
        code = 500
        error_string = ("500 Internal Server Error: "
                        "The server has encountered a situation it doesn't know how to handle.")
    return jsonify(error=error_string), code

from app import views  # pylint: disable=wrong-import-position

if __name__ == "__main__":  # pragma: no cover
    app.run()
