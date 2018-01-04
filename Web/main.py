#!/usr/bin/env python3
from bottle import get,post,run,request,template
from socket import *
@get("/web")
def index():
    return template("index")
@post("/cmd")
def cmd():
    print("BUTTON_DOWN: "+request.body.read().decode())

    HOST='127.0.0.1'
    PORT=9999

    s = socket(AF_INET,SOCK_DGRAM)
    s.connect((HOST,PORT))
    #while True:

    message = request.body.read().decode()
    s.sendall(message)
    #data = s.recv(1024)
    #print data
    
    s.close()
    return "OK"
run(host="0.0.0.0",port=8081)
