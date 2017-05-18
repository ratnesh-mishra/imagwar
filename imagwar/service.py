__author__ = 'ratnesh.mishra'
from wand.image import Image

from wand.color import Color
from aiohttp.web import Request, Response
from aiohttp import web
import asyncio
from .handler import Helper
from aiohttp.web import HTTPOk, HTTPBadRequest
import json
import os


class Imagwar:

    def __init__(self, helper, config):
        self._helper = helper
        self._config = config


    @asyncio.coroutine
    def upload_file(self, request: Request):
        """
        Need to exhibit different behaviour for pdfs and other files
        """
        url = None
        payload = yield from request.post()
        # Need to figure how to get file name only
        file = payload['file']
        file_name = file.filename
        extension = self._helper.get_file_type(file_name)
        full_path = '/tmp/'+file_name
        if extension == 'image':
            f = open(full_path, 'wb')
            _ = f.write(file.file.read())
            url = self._get_transformed_url(file_name, full_path, payload)

        else:
            # name = yield from self._helper.get_filename_from_specs(filename)
            url = yield from self._helper.upload_file(file_name,full_path)

        return Response(status=200, content_type='application/json', body=json.dumps({"url": url}).encode())

    @asyncio.coroutine
    def transform_image(self, request):

        pass

    def _get_transformed_url(self, f_name, full_path, specs):
        """

        :param file_name: Name of the file to be transformed
        :param specs: specification of the output file to be returned
        :return: Image url for the new image
        """
        _format = f_name.split('.')[-1]
        f_name = f_name[0:f_name.rfind('.')]
        with Image(filename=full_path) as img:
                quality = int(specs.get('quality', 100))
                height = int(specs.get('height', img.height))
                width = int(specs.get('width', img.width))
                _format = specs.get('format', _format)
                with img.clone() as i:
                    i.compression_quality = quality
                    i.resize(height, width)
                    i.format = _format
                    _file_name = 'q_{quality},h_{height},w_{width}:{name}.{format}'.format(quality=quality, height=height,
                                                                                           width=width, name=f_name,
                                                                                           format=_format)
                    full_path = '/tmp/'+_file_name
                    f = open(full_path, 'wb')
                    i.save(file=f)
                    # name = yield from self._helper.get_filename_from_specs(filename)
                    return self._helper.upload_file(_file_name, '/tmp/'+_file_name)


    def upload_image(self):
        pass


if __name__ == '__main__':
    config = json.load(open('./config.json'))
    access_key = config['S3_ACCESS_KEY_ID']
    secret = config['S3_SECRET_ACCESS_KEY']
    bucket = config['S3_BUCKET']
    port = config['Port']
    app = web.Application()
    loop = asyncio.get_event_loop()
    helper = Helper(access_key, secret, bucket)
    image_service = Imagwar(helper, config)
    app.router.add_route('POST', '/upload-file', image_service.upload_file)
    app.router.add_route('GET', '/transform-image', image_service.transform_image)
    serve = loop.create_server(app.make_handler(), '0.0.0.0', port)
    loop.run_until_complete(serve)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Closing")
        loop.stop()



