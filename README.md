# homework3
This is a homework to check.
This is executable in Python3 .
Tested in Python 3.5.2, 3.6.8, 3.6.9 .
This code contains basics to a framework achitecture approach. An unusul framework behaveour is added here: you can create your own location handlers to built your own site, as well as grab the existant html code (and it's dependences) in order to use your own location handlers, and auto-generated location handlers together. Auto-generated handlers is formed by a dynamic_handler handler function. To create a static handler, you can add a handler function similar to a test_handler function.
## Usage. ##
cd homework3 && uwsgi --http :9090 --wsgi-file start.py
Then browse localhost:9090 in your browser.
## Python files meaning. ##
start.py -- the main and the only file.
project -- a build-in example that is commited.
