from controllers.user.UserController import UserController
# from middlewares.RoleMiddleware import RoleMiddleware
from middlewares.SessionKeyMiddleware import SessionKeyMiddleware

user_routes = [
    {
        "method": "GET",
        "group": [
            {
                "method": "GET",
                "path": "/",
                "handler": UserController.list,

                # m = 1    
                # "middleware": SessionKeyMiddleware

                # m = 2
                # "middleware": 'session',

                # m =3
                # "middleware": [SessionKeyMiddleware, 'xyz'],

                # m = 4 
                # "middleware": 'session:admin',

                # m = 5
                "middleware": 'session:session=123',
            },
            {
                "method": "POST",
                "path": "/",
                "handler": UserController.create
            },
            {
                "method": "GET",
                "path": "/{id}",
                "handler": UserController.get
            },
            {
                "method": "PUT",
                "path": "/{id}",
                "handler": UserController.update
            },
            {
                "method": "DELETE",
                "path": "/{id}",
                "handler": UserController.delete
            },
        ]
    }
]
