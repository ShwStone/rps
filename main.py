from http.server import HTTPServer, BaseHTTPRequestHandler
from agent import Agent
import time
import threading

agents = {}
lastActive = {}

class Request(BaseHTTPRequestHandler) :
    def do_GET(self) :
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()

        params = self.path.split('?')[-1]
        id = params.split('=')[-1]

        if id not in agents :
            agents[id] = Agent()

        self.wfile.write(bytes(str(
            agents[id].round()
        ), encoding='UTF-8'))

    def do_POST(self) :
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        
        body = self.rfile.read(
            int(self.headers['content-length'])
        ).decode("UTF-8")

        params = self.path.split('?')[-1]
        id = params.split('=')[-1]

        lastActive[id] = time.time()

        if body != 'alive' :
            if id not in agents :
                agents[id] = Agent()

            playerAction, agentAction, result = map(int, body.split(','))
            agents[id].result(playerAction, agentAction, result)

def checkAlive() :
    threading.Timer(600, checkAlive).start()
    currentTime = time.time()

    deads = []
    for id, lastActiveTime in lastActive.items() :
        if currentTime - lastActiveTime > 300 :
            deads.append(id)
    
    for id in deads :
        lastActive.pop(id)
        agents.pop(id)

host = ('localhost', 8899)
server = HTTPServer(host, Request)

print("Serving backend on localhost:8899 ...")
checkAlive()

server.serve_forever()

