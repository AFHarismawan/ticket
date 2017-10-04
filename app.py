from apistar.frameworks.wsgi import WSGIApp as App
from project.routes import routes

app = App(routes=routes)

if __name__ == '__main__':
    app.main()