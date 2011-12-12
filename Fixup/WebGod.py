import os
from tornado.web import Application, RequestHandler, StaticFileHandler
from tornado.httpserver import HTTPServer
from tornado import template 
from tornado.wsgi import WSGIContainer
from tornado.ioloop import IOLoop
from GodBits import *

class MainHandler(RequestHandler):

    def __init__(self, request, response, query_engine):
        super(MainHandler, self).__init__(request, response)
        self.query_engine = query_engine 

    def get(self):
        loader = template.Loader("./") 
        self.write(loader.load("WebGod.html").generate(question=None, answer=None, files=None))

    def post(self):
        loader = template.Loader("./") 
        question = self.get_argument("question", default=[], strip=True)
        if question != None:
            self.query_engine.question(question)
            self.write(loader.load("WebGod.html").generate(answer=self.query_engine.answer(), question=question, files=None))

        #files = self.request.files
        #if files != None:
        #    self.write(loader.load("WebGod.html").generate(answer=self.query_engine.answer(), files=None))

if __name__ == "__main__":
    gobits=Gobits()
    glubits=Glubits()
    query_engine = Query(gobits, glubits)

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static")
    }
    application = Application([
        (r"/", MainHandler, dict(query_engine=query_engine)), 
        (r"/(logo.jpg)", StaticFileHandler,
         dict(path=settings['static_path'])),
        ], **settings)
    http_server = HTTPServer(application)
    http_server.listen(8080)
    IOLoop.instance().start()
