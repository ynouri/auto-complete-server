"""Tornado web server."""
# pylint: disable=W0223
import os
import tornado.ioloop
import tornado.web
from auto_complete_server.models.mpc import MostPopularCompletionModel


TEST_CORPUS_FILE = os.path.join("data", "test_conversations.json")
MPC = MostPopularCompletionModel(max_completions=3)
MPC.build_trie(TEST_CORPUS_FILE)


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
    return tornado.web.Application(
        [(r"/autocomplete", AutoCompleteHandler), (r"/", MainHandler)],
        autoreload=True,
    )


if __name__ == "__main__":
    # Create and start web app
    APP = make_app()
    APP.listen(13000)
    tornado.ioloop.IOLoop.current().start()
