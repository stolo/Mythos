#!/usr/bin/python

def application(environ, start_response):
    status = '200 OK'
    output = 'Hello World!'

    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(output)))]
    start_response(status, response_headers)

    return [output]

if __name__ == "__main__": 
    from tornado.httpserver import HTTPServer 
    from tornado.wsgi import WSGIContainer 
    from tornado.ioloop import IOLoop 
    http_server = HTTPServer(WSGIContainer(application)) 
    http_server.listen(8080) 
    IOLoop.instance().start()
