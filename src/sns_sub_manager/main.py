from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_health import health
from starlette.responses import RedirectResponse

from .config import get_config
from .routes import ROUTERS
from .utils.logging import get_logger
from .utils.logging import setup_logger


# Setup the FastAPI app object
app = FastAPI(
    title="sns-sub-manager",
    version="0.0.1",
    description="A REST API to manage SNS Queues",
)

# This adds a basic health check route for deploying in k8s. Right now, does no checks, just 200s
app.add_api_route("/health", health([]))
for router in ROUTERS:
    app.include_router(router)

config = get_config()
setup_logger(config)
logger = get_logger()

if config.enable_cors:
    logger.debug("Enabling CORS")
    options = {
        "allow_credentials": config.cors_allow_credentials,
        "allow_methods": config.cors_allow_methods,
        "allow_headers": config.cors_allow_headers,
        "max_age": config.cors_max_age,
    }
    if config.cors_origin_regex is not None:
        logger.debug("Enabling regex origin %s", config.cors_origin_regex)
        options["allow_origin_regex"] = config.cors_origin_regex
    else:
        logger.debug("Enabling CORS origins %s", config.cors_origins)
        options["allow_origins"] = config.cors_origins
    app.add_middleware(CORSMiddleware, **options)


@app.on_event("startup")
async def startup_tasks():  # pragma: no coverage
    """Sets up our redis store and adds all the models to it"""
    pass


@app.get("/")
def docs_redirect():
    """Redirects 307 to /docs"""
    return RedirectResponse(url="/docs/")
