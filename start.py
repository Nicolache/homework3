import os

from http.client import responses
from typing import Generator, Dict, Callable, Union, Any

handlers_map_type = Dict[str, Callable]
response_type = Dict[str, Any]
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
# response: response_type = {}
response = {}  # type: Dict[str, Any]


def among_project_extensions(filename):
    """Checks if filename belongs to registered extensions.

    Keyword arguments:
    filename -- a string with filename.

    Return type is bool.
    """
    return filename.split('.')[1].lower() in datakinds.keys()


def search_project_files() -> Generator[str, None, None]:
    """Generates all files locations inside `projectpath` location.

    Returns a generator.
    """
    for dirname, dirs, files in os.walk(projectpath, topdown=True):
        for file in files:
            if among_project_extensions(file):
                yield os.path.join(dirname, file)


def read_file_content(diskpath: str, datakind: str) -> text_or_bytes_type:
    """Reads a given file content, and returns it as a string, or bytes.

    Keyword arguments:
    diskpath -- a path to file.
    datakind -- tells if a given file is a file of strings, or of bytes.

    The return type is str, of bytes.
    """
    diskfilehandler = open(diskpath, datakind)
    file_content = diskfilehandler.read()
    return file_content


def map_handler(filename):
    """Makes a handler of a file with a given filename. It stores it to
    handlers_map and maps a local www location to it.

    Keyword arguments:
    filename -- path to file.
    """
    location = filename[len(projectpath) - 1:]
    handlers_map[location] = dynamic_handler


def auto_map_handlers():
    """Searches all the files by the path stored in projectpath variable,
    and makes handlers of these files.
    """
    handlers_map['/'] = dynamic_handler
    for filename in search_project_files():
        map_handler(filename)


def dynamic_handler(env):
    """The function emulates a static handler behaveour
    according to static files found in project's directory projectpath.

    Keyword arguments:
    env -- a dictionary of parameters that were got with the client's request.

    The return type is dict.
    """
    filename = projectpath[:-1] + env['PATH_INFO']
    if filename == projectpath:
        filename = projectpath + 'index.html'
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
    """This is a handler
    The return type is dict.
    """
    return {
        'text': b'The page is not found.',
        'status_code': 404
    }


def test_handler(env):
    """This is a custom handler for a certain location.
    It's aimed to generate a desired response, as html, css, etc. ..
    Plenty of similar handlers could be made to build your site.
    """
    return {
        'text': b'This is a test location.',
        'status_code': 200
    }


handlers_map['/test'] = test_handler


def get_code_string(status_code):
    """It produces strings of a kind: 200 OK, 301 Moved Permanently, etc. ...

    Keyword arguments:
    status_code -- a number of status code.

    The return type is str.
    """
    code_number_and_str = '{} {}'.format(
        status_code,
        responses[status_code]
    )
    return code_number_and_str


def application(env, start_response):
    """The default function that the uWSGI Python loader will search.

    Keyword arguments:
    env -- a dictionary of parameters that were got with the client's request.
    start_response -- A built-in function uwsgi_spit.
    """
    global mapped
    if not mapped:
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
