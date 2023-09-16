import logging
import os
import signal
import sys
import threading
import falcon
from wsgiref.simple_server import make_server
from adjektiver import Adjektiver

global ordliste
ordliste = None
global server
server = None



logging.basicConfig(filename="wordslog",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)




class WordResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        
        alder = req.params.get("alder", 100)
    
        adj1, adj2 = ordliste.hent_adjektiver(alder)
        
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = f'{adj1}, {adj2} og {alder}'
        print(resp.text)
        logging.info(f"Req from {req.remote_addr} got \"{resp.text}\"")

class Server:
    def __init__(self, port, app) -> None:
        self.port = port
        self.server = make_server('', port, app)
        self.server_thread = threading.Thread(target=self.run, name="server")
        self.server_thread.daemon = True

        signal.signal(signal.SIGTERM, self.shutdown_on_signal)
        signal.signal(signal.SIGINT, self.shutdown_on_signal)

    def start(self):
        self.server_thread.start()
        self.server_thread.join()

    def run(self):
        print(f"Running server on port {self.port}.")
        self.server.serve_forever()
        print("Done")

    def shutdown_on_signal(self, signum, frame):
        if hasattr(signal, "Signals"):
            signame = signal.Signals(signum).name
            sigdesc = "{}, {}".format(signum, signame)
        else:
            sigdesc = str(signum)
        if self.server_thread.is_alive():
            print("Shutting down ... ", end="")
            self.server.shutdown()
            self.server_thread.join(5)
        sys.exit(1)

if __name__ == '__main__':

    port = 23232
    app = falcon.App()
    app.add_route('/ord', WordResource())
    ordliste = Adjektiver()
    Server(port, app).start()