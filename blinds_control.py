# server stuff
import simple_server as simpleSrvr
from simple_server import *
# motor control stuff
import motor_control as motorCtrl

def motor_get(self):
    motorCtrl.move_wheel({1:500})


motorHandler = simpleSrvr.funHandler
# motorHandler.do_GET = motor_get
motorHandler.do_GET = motorHandler.do_GET(simpleSrvr.funHandler, motor_get)


httpd = SocketServer.TCPServer(("", port), motorHandler)
httpd.serve_forever()