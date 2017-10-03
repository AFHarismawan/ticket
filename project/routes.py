from apistar import Include, Route
from apistar.docs import docs_routes
from apistar.statics import static_routes
from project.api.auth import login, register
from project.api.event import event, event

routes = [
    Route('/login', 'GET', login),
    Route('/register', 'POST', register),
    Route('/event', 'POST', event),
    Route('/event', 'GET', event),
    Include('/docs', docs_routes),
    Include('/static', static_routes)
]
