from middlewares.SessionKeyMiddleware import SessionKeyMiddleware

middleware_config = {
    "middlewares": {
        "aliases": {
            "session": SessionKeyMiddleware,
        }
    }
}