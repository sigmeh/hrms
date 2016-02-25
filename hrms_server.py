#!/usr/bin/env python
import BaseHTTPServer, CGIHTTPServer, cgitb
def main():
	cgitb.enable()  # CGI error reporting enabled
	server=BaseHTTPServer.HTTPServer
	handler=CGIHTTPServer.CGIHTTPRequestHandler
	server_address=("", 8000)
	handler.cgi_directories=["/",'/cgi-bin','/static']
	httpd=server(server_address, handler)
	httpd.serve_forever()
if __name__ == '__main__':
	main()