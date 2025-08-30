"""
This module contains the Flask application factory.
"""
from __future__ import annotations

from flask import Flask

from .cache import cache
from .routes import main


def create_app() -> Flask:
    """
    Creates and configures a Flask application instance.
    The application factory pattern is used to make the application
    more modular and testable.
    """
    app = Flask(
        __name__,
        template_folder="../templates",
    )

    # Load configuration from a .env file
    if not app.config.from_prefixed_env():
        print(
            "Warning: Failed to load configuration from environment variables."
        )

    # Initialize extensions
    cache.init_app(app)  # type: ignore

    # Register blueprints
    app.register_blueprint(main)

    return app
