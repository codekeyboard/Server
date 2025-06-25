from core.Middleware import Middleware

class SessionKeyMiddleware(Middleware):

    def __init__(self, *args, **kwargs):
        self.token = args[0] if args else None
        self.sessionm = kwargs.get("sessionm")

    async def next(self, request, handler):
        # check if request has 'session' in query params or json body
        session_key = request.query_params.get('session')
        if not session_key: return self.unauthorized_response()
        print(f"SK = {session_key}")
        return await handler(request)

    def unauthorized_response(self):
        return {"error": "Unauthorized"}, 401

    def forbidden_response(self):
        return {"error": "Forbidden"}, 403


