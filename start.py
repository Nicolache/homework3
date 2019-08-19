import os

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
    'html': 'r',
    'css': 'r',
    'js': 'r',
    'gif': 'rb',
    'jpg': 'rb',
    'jpeg': 'rb',
    'mp3': 'rb',
    'png': 'rb'
}
mapped = False
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
                yield os.path.join(dirname, file)[len(projectpath):]


def alter_page_content():
    pass


def read_file_content(diskpath: str, datakind: str) -> text_or_bytes_type:
    diskfilehandler = open(diskpath, datakind)
    file_content = diskfilehandler.read()
    return file_content


def map_handler(filename):
    print(filename)
    extension = filename.split('.')[1]
    print(extension)
    datakind = datakinds.get(extension)
    handlers_map[filename] = dynamic_handler(read_file_content(
        filename,
        datakind
    ))


def auto_map_handlers():
    for filename in search_project_files():
        map_handler(filename)


def dynamic_handler(env, data):
    """The function emulates a static handler behaveour
    according to static files found in project's directory.
    """
    return {'text': data}


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
    print(mapped)
    if mapped == False:
        mapped = True
        auto_map_handlers()
    print('PATH ' + env['PATH_INFO'])
    print(handlers_map)
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


def search_files_test():
    for file in search_project_files():
        print(type(file))
        print(file)


def main():
    # search_files_test()
    pass


if __name__ == '__main__':

    main()
