__author__ = 'ratnesh.mishra'
import boto
from asyncio import coroutine

""" Collection of utility methods gor imagwar """

image_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif']


class Helper:

    def __init__(self, access_key, secret, bucket):
        conn = boto.connect_s3(access_key, secret)
        self.bucket = conn.get_bucket(bucket)

    def upload_file(self, filename, full_path):
        key = self.bucket.new_key(filename)
        key.set_contents_from_filename(full_path)
        key.set_acl('public-read')
        url = key.generate_url(expires_in=7, query_auth=False)
        return url

    def get_file_type(self, filename):
        extension = filename.split('.')[-1].lower()
        if extension in image_extensions:
            return 'image'
        else:
            return 'other'



    # def get_file_name_from_specs(self, filename):
    #     pass
