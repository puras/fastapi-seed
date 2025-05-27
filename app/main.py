import os
import sys

from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import pipmaster as pm

from app.conf import settings
from app.core.logging import setup_logging
from app.route import create_routes
from app.util import check_env_file, parse_args, display_splash_screen


def create_app() -> FastAPI:
    app_kwargs = {
        "title": settings.PROJECT_NAME,
        "description": settings.PROJECT_DESCRIPTION,
        "version": settings.VERSION,
        "openapi_url": f"{settings.API_V1_STR}/openapi.json",
        "docs_url": f"{settings.API_V1_STR}/docs",
        "redoc_url": f"{settings.API_V1_STR}/redoc",
        "openapi_tags": [{"name": "api"}]
    }

    app = FastAPI(**app_kwargs)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 路由注册
    app.include_router(create_routes(), prefix=settings.API_V1_STR)

    # 全局异常处理
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": str(exc.detail),
                "data": None
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "code": 422,
                "message": "数据验证失败",
                "data": str(exc.errors())
            }
        )

    # @app.get("/health")
    # async def health_check():
    #     return {
    #         "code": 200,
    #         "message": "success",
    #         "data": {
    #             "status": "healthy",
    #             "version": settings.VERSION
    #         }
    #     }
    return app

def check_and_install_dependencies():
    required_packages = [
        "unicon",
        "fastapi",
    ]
    for package in required_packages:
        if not pm.is_installed(package):
            print(f"Installing {package}...")
            pm.install(package)
            print(f"{package} installed successfully.")

def main():
    if "GUNICORN_CMD_ARGS" in os.environ:
        print("Running under Gunicorn - worker management handled by Gunicorn.")
        return

    if not check_env_file():
        sys.exit(1)

    setup_logging()

    args = parse_args(is_uvicorn_mode=True)
    display_splash_screen(args)

    # Start Uvicorn in single process mode
    import uvicorn

    uvicorn_config = {
        "host": args.host,
        "port": args.port,
        "log_config": None,
    }

    if settings.DEBUG:
        print("Starting Uvicorn server in development mode.")
        uvicorn_config["app"] = "app.main:create_app"
        uvicorn_config["factory"] = True
        uvicorn_config["reload"] = settings.DEBUG
    else:
        print("Starting Uvicorn server in production mode.")
        app = create_app()
        uvicorn_config["app"] = app

    print(f"Starting Uvicorn server in single-process mode on {args.host}:{args.port}.")
    uvicorn.run(**uvicorn_config)

if __name__ == "__main__":
    main()