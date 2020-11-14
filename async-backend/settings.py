import os

import uvloop

uvloop.install()

DEBUG = os.environ.get("DEBUG", "").lower() == "true"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

ALLOWED_METHODS = os.getenv("ALLOWED_METHODS", "").split(",")
if not ALLOWED_METHODS:
    ALLOWED_METHODS = ["*"]

MODELS_DIR = os.getenv("MODELS_DIR", "/models")
