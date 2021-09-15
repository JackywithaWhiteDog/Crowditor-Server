"""Endpoint routing for the application.

This module define the router to each endpoints.

"""
from app import api, docs
from app.views.health import HealthAPI
from app.views.overview import OverviewAPI
from app.views.advice import AdviceAPI
from app.views.project_list import ProjectListAPI
from app.views.project import ProjectAPI
from app.views.estimation import EstimationAPI

api.add_resource(HealthAPI, '/health')
docs.register(HealthAPI)

api.add_resource(OverviewAPI, '/overview')
docs.register(OverviewAPI)

api.add_resource(AdviceAPI, '/advice')
docs.register(AdviceAPI)

api.add_resource(ProjectListAPI, '/projects')
docs.register(ProjectListAPI)

api.add_resource(ProjectAPI, '/projects/<int:project_id>')
docs.register(ProjectAPI)

api.add_resource(EstimationAPI, '/estimation')
docs.register(EstimationAPI)
