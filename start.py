from http.client import responses
from typing import Generator, Dict, Callable, Union


handlers_map_type = Dict[str, Callable]
text_or_bytes_type = Union[str, bytes]

content_type_convert_dictionaty = {
    'html': 'text/html',
    'jpg': 'image/jpg',
}
handlers_map: handlers_map_type = {}
response = {}


def search_project_files() -> Generator[str, None, None]:
    pass


def alter_page_content():
    pass


def add_handler():
    pass


def read_file_content(diskpath: str, datakind: str) -> text_or_bytes_type:
    diskfilehandler = open(diskpath, datakind)
    file_content = diskfilehandler.read()
    return file_content


def auto_add_handlers():
    for files in search_project_files():
        print(files)
        add_handler()


def dynamic_handler():
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
