import json
import boto3



from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
import tornado

class ExampleRoute(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        self.finish(json.dumps({
            "data": "This is /jupS3/get-example endpoint!"
        }))

class S3BucketContents(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        listOfFiles = ["first-file", "second-file", "third-file"]
        self.finish(json.dumps({
            "data": listOfFiles
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupS3", "get-example")
    route_pattern_s3 = url_path_join(base_url, "jupS3", "get-bucket-contents")

    handlers = [(route_pattern, ExampleRoute), (route_pattern_s3, S3BucketContents)]
    web_app.add_handlers(host_pattern, handlers)
