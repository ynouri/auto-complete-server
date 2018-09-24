"""Tornado web server."""
# pylint: disable=W0223
import os
import logging
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import tornado.options
from auto_complete_server.models.mpc import MostPopularCompletionModel


DEFAULT_TRIE_FILE = os.path.join("models", "test_conversations.trie")
define("trie-file", DEFAULT_TRIE_FILE, help="Trie file to load")
define("port", 13000, help="Port to listen on")
define("autoreload", False, help="Enable auto-reload")

# Instantiate model at module level
MPC = MostPopularCompletionModel(max_completions=3)


class AutoCompleteHandler(tornado.web.RequestHandler):
    """Handle auto-complete requests and returns completions json."""

    def get(self, *args, **kwargs):
        """Handle get requests."""
        prefix = self.get_argument("q")
        completions = {"completions": MPC.generate_completions(prefix)}
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header("Access-Control-Allow-Origin", "*")
        self.write(completions)


class MainHandler(tornado.web.RequestHandler):
    """Serve the web service main page."""

    def get(self, *args, **kwargs):
        """Render a client page, without templating."""
        self.render("static/client.html")


def make_app():
    """Instantiate the Tornado web application with settings and routes."""
    MPC.load(options.trie_file)
    app = tornado.web.Application(
        [(r"/autocomplete", AutoCompleteHandler), (r"/", MainHandler)],
        autoreload=options.autoreload,
    )
    return app


if __name__ == "__main__":
    tornado.options.parse_command_line()
    APP = make_app()
    APP.listen(options.port)
    logging.info("Web server listening on %s", options.port)
    tornado.ioloop.IOLoop.current().start()
