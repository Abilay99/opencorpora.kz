from flask import Flask
from flask_cors import CORS
from auth_service_api.api import auth, v1
from auth_service_api.extensions import apispec
from auth_service_api.extensions import db
from auth_service_api.extensions import jwt
from auth_service_api.extensions import pagination
from auth_service_api.extensions import migrate

def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("auth_service_api")
    app.config.from_object("auth_service_api.config")
    app.config['PAGINATE_PAGINATION_OBJECT_KEY'] = None
    app.config['PAGINATE_DATA_OBJECT_KEY'] = "results"
    app.config['PAGINATE_PAGE_SIZE'] = 3

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    CORS(app)

    return app


def configure_extensions(app):
    """configure flask extensions"""
    pagination.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(v1.views.blueprint)

app = create_app(testing=False)
