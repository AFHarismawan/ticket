from apistar import Include, Route
from apistar.handlers import docs_urls, static_urls
from project.api.auth import login, register
from project.api.event import add_event, get_event

routes = [
    Route('/login', 'GET', login),
    Route('/register', 'POST', register),
    Route('/event', 'POST', add_event),
    Route('/event', 'GET', get_event),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]
