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

s3 = boto3.client(
        's3',
        endpoint_url='https://object-store-api.infra.aurin-prod.cloud.edu.au')
def list_files_in_bucket(bucket_name):
    response = s3.list_objects_v2(Bucket=bucket_name)

    if 'Contents' in response:
        files = [item['Key'] for item in response['Contents']]
        return files
    else:
        return []

class S3BucketContents(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):
        listOfFiles = list_files_in_bucket('infra-test-1')
        self.finish(json.dumps({
            "data": listOfFiles
        }))

class createOrAppendToFile(APIHandler):
    # The following decorator should be present on all verb methods (head, get, post,
    # patch, put, delete, options) to ensure only authorized user can request the
    # Jupyter server
    @tornado.web.authenticated
    def get(self):

        print(os.getcwd());
        bucket_name = 'infra-test-1'
        file_name = self.get_argument('file', 'default-file')
        print("filename:", file_name)
        download_path = os.path.join(os.getcwd(), file_name.split("/")[-1])

        try:
            s3.download_file(bucket_name, file_name, download_path)
        except Exception as e:
            print(e)

        self.finish(json.dumps({
            "data": "listOfFiles"
        }))


def setup_handlers(web_app):
    host_pattern = ".*$"

    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupS3", "get-example")
    route_pattern_s3 = url_path_join(base_url, "jupS3", "get-bucket-contents")
    route_pattern_create_or_append = url_path_join(base_url, "jupS3", "create-or-append-to-file")
    handlers = [(route_pattern, ExampleRoute), (route_pattern_s3, S3BucketContents), (route_pattern_create_or_append, createOrAppendToFile)]
    web_app.add_handlers(host_pattern, handlers)
