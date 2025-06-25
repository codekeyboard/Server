import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from piccolo.engine import engine_finder
from contextlib import asynccontextmanager
from routes.routes import routes  
from core.Middleware import Middleware
from util.config import config

# Lifespan for DB connection pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = engine_finder()
    await engine.start_connection_pool()
    yield
    await engine.close_connection_pool()

# Initialize FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Logging setup

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

# CORS middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization", "token"]
)

# Global Exception Handlers

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An unexpected error occurred", "error": str(exc)},
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    logger.warning(f"404 Not Found: {request.url}")
    return JSONResponse(
        status_code=404,
        content={"message": "Route not found", "error": str(exc)},
    )

# Middleware registration decorator
def register_middleware(middleware=None, middleware_args=[], middleware_kwargs={}):
    
    def middleware_decorator(handler):

        if not middleware: return handler
        if not (isinstance(middleware, type) and issubclass(middleware, Middleware)):
            raise ValueError("Middleware must be a subclass of Middleware")

        async def middleware_wrapper(request: Request):
            return await middleware(*middleware_args, **middleware_kwargs).next(request, handler)
        
        return middleware_wrapper

    return middleware_decorator

# Route registration

def register_route(method, path, handler, middleware=None):
    print(f"Registering middleware: {middleware}")
    async def endpoint(request: Request):
        return await handler(request)
    
    def add_middleware(middleware):
        nonlocal endpoint

        if isinstance(middleware, type) and issubclass(middleware, Middleware):
            endpoint = register_middleware(middleware)(endpoint)
            return
        
        if isinstance(middleware, str):
            alias = middleware.split(':')[0]
            middleware_class = config('middlewares.aliases', {}).get(alias)
            if not middleware_class:
                raise ValueError(f"No middleware found with alias {middleware}")

            remaining = middleware[len(alias)+1:]
            args = []
            kwargs = {}

            for arg in remaining.split(','):
                if not arg: continue

                split = arg.split(',')
                if len(split) == 2:
                    k,v = split
                    kwargs[k] = v
                    continue

                args.append(arg)
            endpoint = register_middleware(middleware_class, args, kwargs)(endpoint)
            return

        if not isinstance(middleware, list):
            raise ValueError(f"Expected middleware in route, found {type(middleware)}")
        
        if len(middleware) != 2:
            for m in middleware:
                add_middleware(m)
            return

        first = middleware[0]
        second = middleware[1]

        if not (isinstance(first, type) and issubclass(first, Middleware)):
            add_middleware(first)
            add_middleware(second)
            return
        
        if isinstance(second, dict):
            endpoint = register_middleware(first, middleware_kwargs=second)(endpoint)
            return
        
        if isinstance(second, list):
            endpoint = register_middleware(first, middleware_args=second)(endpoint)
            return
        
        if isinstance(second, type) and issubclass(second, Middleware):
            endpoint = register_middleware(second)(endpoint)
            endpoint = register_middleware(first)(endpoint)
            return

        endpoint = register_middleware(first, middleware_args=[second])(endpoint)
        

    if middleware:
        add_middleware(middleware)                


    app.add_api_route(
        path,
        endpoint,
        methods=[method],
        name=f"{method}_{path.replace('/', '_')}"
    )
    logger.debug(f"Registered route: {method} {path}")

def bind_routes(base_path, routes_list):
    for route in routes_list:
        full_path = base_path + route.get("path", "")
        if "group" in route:
            bind_routes(full_path, route["group"])
        else:
            register_route(
                method=route["method"],
                path=full_path,
                handler=route["handler"],
                middleware=route.get("middleware")
            )

# Root Endpoint

@app.get("/")
async def root():
    return {"message": "API is up and running!"}

# ---------------
# Bind All Routes
# ---------------

bind_routes("", routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=7002, reload=True)
