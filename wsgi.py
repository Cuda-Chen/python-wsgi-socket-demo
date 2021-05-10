import socket
from wsgiref import simple_server

def serve(app):
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(('', 8080))
    listener.listen(5)
    while True:
        s, addr = listener.accept()
        request = s.recv(10000)
        print(f'request text: {request}')
        method, rest = request.decode().split(' ', 1)
        path, rest = rest.split(None, 1)
        def start_reponse(status, headers):
            print('sending headers')
            front_matter = '\r\n'.join(['HTTP/0.9 '+status] + [k+': '+v for k, v in headers])
            s.send(front_matter.encode())
            s.send(b'\r\n\r\n')
        environ = {'REQUEST_METHOD': method, 'PATH_INFO': path}
        for data in app(environ, start_reponse): # WSGI specifies that an iterator should be returned
            print('sending data')
            s.send(data)
        s.close()

def wsgihandler(environ, start_reponse):
    """WSGI application"""
    start_reponse("200 OK", [('Content-Type','text/plain')])
    #r = Request(environ)
    return [('You asked to '+environ['REQUEST_METHOD']+' '+environ['PATH_INFO']).encode(), 
            b' some more data',
            b'\r\n']

if __name__ == '__main__':
    serve(wsgihandler)
