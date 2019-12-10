#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import cgi
import socket
import urllib.parse as urlparse
#if you run in Python 2 just replace http.server with BaseHTTPServer
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
import base64


def ReadFile(filename):
    file_object = open(filename, "rb")
    try:
        fileContent = file_object.read()
    finally:
        file_object.close()
    return fileContent


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        requests = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        node = self.path.split('?')
        node = node[0]
        print("Request node = " + str(node))
        
        #Process header
        self.send_response(200)
        try:
            if node.split('.')[-1] == "html" or node.split('.')[-1] == "htm":
                print("Html files, set header Content-Type=text/html")
                self.send_header('Content-type', 'text/html')
        except:
            pass
        self.end_headers()
        #--Process header
#------------------Web Services Start-----------------
        # A example of hello world, request URL is http://your.server/requestnode?hello=World:
        if node == "/requestnode": 
            self.wfile.write(("Hello, "+str(requests["hello"][0])).encode())

#------------------Web Services End-----------------

#------------------Web Server Load File From File System Start-----------------
        elif node == "/":
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/WEBCONTENT/index.html")
                self.wfile.write(filecontent)
                print("Return file: " + node)
            except:
                print("File not found: " + node)
                self.wfile.write(("<html><title>404 Not Found</title>404 Error<br>File /index.html Not Found.</html>").encode())
        else:
            try:
                filecontent = ReadFile(os.path.split(os.path.abspath(__file__))[0] + "/WEBCONTENT" + node)
                self.wfile.write(filecontent)
                print("Return file: " + node)
            except:
                print("File not found: " + node)
                self.wfile.write(("<html><title>404 Not Found</title>404 Error<br>File " + node + " Not Found.</html>").encode())



#------------------Web Server Load File From File System End-----------------

    def do_POST(self):
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD': 'POST'})

        value = form.getvalue("key")

        #self._set_headers()
        self.wfile.write("Post key" + value)


def run(server_class, handler_class, port):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Fucking http server is started.")
    httpd.serve_forever()


#————————SQLike Connector, if you don't nood you can remove it————————
def SQLike_Query(cmdstring):
    global sqlikesock
    sqlikesock.send(cmdstring)
    data = sqlikesock.recv(1024)
    return data


#————————SQLike Connector, if you don't nood you can remove it————————

if __name__ == "__main__":
    #————————SQLike, if you don't nood you can remove it————————
    global sqlikesock
    sqlikesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sqlikesock.connect(('127.0.0.1', 1667))
        print("SQLike Server Connected!")
    except:
        print("Failed to Connect SQLike DB Server")
    #————————SQLike, if you don't nood you can remove it————————
    run(HTTPServer, S, 8081)
