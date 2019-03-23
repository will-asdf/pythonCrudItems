from flask import Flask
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from Endpoints import Item_endpoints as endpoints
from Utils import Utilities as utils
from flask_cors import CORS

try:
    # Obtener información del archivo de configguración
    configuration = utils.get_config()

    # levantar servicios del crud de items
    app = Flask(__name__)
    CORS(app)

    crud_endpoints = endpoints.define_endpoints(configuration)
    app.register_blueprint(crud_endpoints, url_prefix="/crud")

    server_config = configuration["server"]
    host = server_config["host"]
    port = server_config["port"]
    debug = server_config["debug"]
    if debug:
        app.run(host=host, port=port, debug=debug)
    else:
        http_server = HTTPServer(WSGIContainer(app))
        http_server.bind(port)
        http_server.start(0)  # forks one process per cpu.
        IOLoop.current().start()

    # Presentar vista
except Exception as ex:
    print(str(ex))
