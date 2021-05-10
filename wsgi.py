import socket

def serve():
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
        print(f'received request, method: {method}, path: {path}')
        s.send(b'HTTP/0.9 200 OK\r\nContent-Type: text/plain')
        s.send(b'\r\n\r\n')
        string = f'You asked to {method} {path}'
        s.send(string.encode())
        s.close()

if __name__ == '__main__':
    serve()
