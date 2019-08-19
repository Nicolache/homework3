from http.client import responses
from typing import Generator, Dict, Callable, Union


handlers_map_type = Dict[str, Callable]
text_or_bytes_type = Union[str, bytes]

content_type_convert_dictionaty = {
    'html': 'text/html',
    'jpg': 'image/jpg',
}
# handlers_map: handlers_map_type = {}
handlers_map = {}
datakinds = {
    '.html': 'r',
    '.css': 'r',
    '.js': 'r',
    '.gif': 'rb',
    '.jpg': 'rb',
    '.jpeg': 'rb',
    '.mp3': 'rb',
    '.png': 'rb'
}
projectpath = './project'
response = {}


def among_project_extensions(filename):
    is_in_extensions = False
    for project_extension in datakinds.keys():
        if filename.endswith(project_extension):
            is_in_extensions = True
    return is_in_extensions


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
    print(filename)
    datakind = datakinds.get(filename.split('.')[1])
    handlers_map[filename] = dynamic_handler(read_file_content(filename, datakind))


def auto_map_handlers():
    for filename in search_project_files():
        map_handler(filename)


def dynamic_handler(data):
    """The function emulates a static handler behaveour
    according to static files found in project's directory.
    """
    pass


def test_handler():
    return {
        'text': 'This is a test location.',
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
    print('PATH ' + env['PATH_INFO'])
    if env['PATH_INFO'] in handlers_map.keys():
        status_code = 200
    else:
        status_code = 404
    code_str = get_code_string(status_code)
    start_response(code_str, [('Content-Type', 'text/html')])
    return [b"Hello World"]
