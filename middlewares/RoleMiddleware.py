from core.Middleware import Middleware

class RoleMiddleware(Middleware):
    def __init__(self, role='any'):
        self.role = role

    def next(self, request, handler):
        # get authorization header
        # get user
        user = User.select(auth_token=header_token)

        if self.role == 'any':
            return handler(request)
            
        elif user.role == self.role:
            return handler(request)

        return self.unauthorized_response()

        # return None
        # return jsonify({"message": "RoleMiddleware initialized with role: " + self.role})
        return handler(request)

    def unauthorized_response(self):
        return {"error": "Unauthorized"}, 401

    def forbidden_response(self):
        return {"error": "Forbidden"}, 403


