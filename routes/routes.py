from routes.users import user_routes

routes = [
    {"method": "GET", "path": "/users", "group": user_routes}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': RoleMiddleware}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': [RoleMiddleware, {'role': 'admin'}]}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': [RoleMiddleware, ['admin']]}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': [RoleMiddleware, 'admin']}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': 'role'}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': 'role:any,api_gate'}
    # {"method": "GET", "path": "/user", "group": user_routes, 'middleware': 'role:role=any,gate=api_gate'}
    
    # {"method": "GET", "path": "/user", "group": user_routes, 'middlewares': [RoleMiddleware, SessionMiddleware]}
]
