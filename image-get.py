from __future__ import annotations
import os, json
from random import randint
from io import StringIO, BytesIO
from PIL import Image
import exiftool
from werkzeug.wrappers import Request, Response
from werkzeug.utils import redirect, send_file, send_from_directory, secure_filename
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound, InternalServerError
from urllib.parse import urlparse 

class ImageService(object):
    def __init__(self, config):
        self.url_map = Map([
            Rule('/', endpoint = 'get_random_image'),
            Rule('/+', endpoint = 'random_image_details'),
            Rule('/<name>', endpoint='get_image_by_name'),
            Rule('/<name>+', endpoint='image_details'),
            Rule('/list', endpoint='list_images'),
        ])
        self.img_directory = "/home/tayler/Documents/repositories/Img/images/"

    def on_get_random_image(self, request):
        fullpath = random_file(self.img_directory)
        # TODO only open once & then convert to bytes on return
        try:
            image = Image.open(fullpath)
            im = open(fullpath, "rb")
        except OSError as e:
            return InternalServerError("unable to open image")

        return send_file(im, request.environ, mimetype = f'image/{image.format}')

    def on_random_image_details(self, request):
        fullpath = random_file(self.img_directory)
        try:
            metadata = get_image_metadata(fullpath)
        except Exception as e:
            return InternalServerError("unable to parse image metadata")
        return Response(metadata, mimetype = f'text/json')

    def on_get_image_by_name(self, request, name):
        name = secure_filename(name)
        return send_from_directory(self.img_directory, name, request.environment)

    def on_image_details(self, request, name):
        name = self.img_directory + secure_filename(name)
        try:
            metadata = get_image_metadata(name)
        except Exception as e:
            return InternalServerError("unable to parse image metadata")
        return Response(metadata, mimetype = f'text/json')

    def on_list_images(self, request):
        img_list = os.listdir(self.img_directory)
        json_res = f"{{ \"images\": {json.dumps(img_list)}}}"
        return Response(json_res, 'text/json')

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, f'on_{endpoint}')(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        print(environ)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

def is_valid_url(url:str)->bool:
    parts = urlparse(url)
    return parts.scheme in ('http', 'https')

def random_file(dirpath:str)->str: 
    files = os.listdir(dirpath)
    return dirpath + files[randint(0, len(files)-1)]

def get_image_metadata(file:str)->str:
    with exiftool.ExifToolHelper() as et:
        metadata = et.execute(file, "-j")
        return metadata

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = ImageService({})
    run_simple('127.0.0.1', 5000, app, use_debugger = True, use_reloader = True)
