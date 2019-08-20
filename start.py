import os

from http.client import responses
from typing import Generator, Dict, Callable, Union

handlers_map_type = Dict[str, Callable]
text_or_bytes_type = Union[str, bytes]

# handlers_map: handlers_map_type = {}
handlers_map = {}
content_types = {
    'html': 'text/html',
    'css': 'text/css',
    'js': 'text/javascript',
    'gif': 'image/gif',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'mp3': 'audio/mpeg3',
}
datakinds = {
    'html': 'r',
    'css': 'r',
    'js': 'r',
    'gif': 'rb',
    'jpg': 'rb',
    'jpeg': 'rb',
    'png': 'rb',
    'mp3': 'rb',
}
mapped = False
projectpath = './project/'
response = {}


def among_project_extensions(filename):
    return filename.split('.')[1].lower() in datakinds.keys()


def search_project_files() -> Generator[str, None, None]:
    """Gets all files locations inside `projectpath` location.

    Returns a generator.
    """
    for dirname, dirs, files in os.walk(projectpath, topdown=True):
        for file in files:
            if among_project_extensions(file):
                yield os.path.join(dirname, file)


def alter_page_content():
    pass


def read_file_content(diskpath: str, datakind: str) -> text_or_bytes_type:
    diskfilehandler = open(diskpath, datakind)
    file_content = diskfilehandler.read()
    return file_content


def map_handler(filename):
    location = filename[len(projectpath) - 1:]
    handlers_map[location] = dynamic_handler


def auto_map_handlers():
    for filename in search_project_files():
        map_handler(filename)


def dynamic_handler(env):
    """The function emulates a static handler behaveour
    according to static files found in project's directory.
    """
    filename = projectpath[:-1] + env['PATH_INFO']
    extension = filename.split('.')[2].lower()
    datakind = datakinds.get(extension)
    data = read_file_content(filename, datakind)
    if extension in ('html', 'css', 'js'):
        data = data.encode("utf-8")
    content_type = content_types.get(extension)
    return {
        'text': data,
        'extra_headers': {'Content-Type': content_type}
        }


def not_found_handler(env):
    return {
        'text': b'The page is not found.',
        'status_code': 404
    }


def test_handler(env):
    return {
        'text': b'This is a test location.',
        'status_code': 200
    }


handlers_map['/test'] = test_handler


def get_code_string(status_code):
    code_number_and_str = '{} {}'.format(
        status_code,
        responses[status_code]
    )
    return code_number_and_str


def application(env, start_response):
    global mapped
    if mapped == False:
        mapped = True
        auto_map_handlers()
    path = env['PATH_INFO']
    response_headers = {'Content-Type': 'text/html'}
    if path in handlers_map.keys():
        handler = handlers_map.get(path)
    else:
        handler = not_found_handler
    response = handler(env)
    status_code = response.get('status_code', 200)
    extra_header = response.get('extra_headers', {})
    response_headers.update(extra_header)
    code_str = get_code_string(status_code)
    start_response(code_str, list(response_headers.items()))
    return [response['text']]
