import json
import boto3
import os


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

class createOrAppendToFile(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        file_name = self.get_argument('file', 'default-file')
        print(file_name)
        listOfFiles = ["first-file", "second-file", "third-file"]

        # Get the user's working directory
        user_dir = os.path.expanduser('~')

        # Create the full file path
        file_path = os.path.join(user_dir, "datathis.txt")

        # Create or append to the file
        with open(file_path, 'a') as f:
            f.write(file_name+'\n')



        self.finish(json.dumps({
            "data": listOfFiles
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupS3", "get-example")
    route_pattern_s3 = url_path_join(base_url, "jupS3", "get-bucket-contents")
    route_pattern_create_or_append = url_path_join(base_url, "jupS3", "create-or-append-to-file")
    handlers = [(route_pattern, ExampleRoute), (route_pattern_s3, S3BucketContents), (route_pattern_create_or_append, createOrAppendToFile)]
    web_app.add_handlers(host_pattern, handlers)
