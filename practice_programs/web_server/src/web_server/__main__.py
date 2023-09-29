# https://docs.python.org/3/howto/sockets.html

import socket
from pathlib import Path
from pprint import pprint

"""
Connection established!
Request: [
    "GET / HTTP/1.1",
    "Host: localhost:8001",
    "User-Agent: curl/8.0.1",
    "Accept: */*",
]
"""

"""
Connection established!
Request:
[   b'GET / HTTP/1.1\r\n',
    b'Host: localhost:8002\r\n',
    b'User-Agent: curl/8.0.1\r\n',
    b'Accept: */*\r\n']

"""

# TODO: Clean shutdown after CTRL+C
"""
OSError: [Errno 98] Address already in use
"""


def main():
    with socket.socket() as s:
        s.bind(("0.0.0.0", 7878))
        s.listen()
        while True:
            c, _ = s.accept()
            print("Connection established!")
            handle_connection(c)


def handle_connection(c):
    # https://docs.python.org/3/library/io.html#module-io
    rfile = c.makefile(mode="rb", buffering=-1)
    # print_request(rfile)
    request_line = rfile.readline().decode().strip()

    if request_line == 'GET / HTTP/1.1':
        status_line = "HTTP/1.1 200 OK"
        filename = "hello.html"
    else:
        status_line = "HTTP/1.1 404 NOT FOUND"
        filename = "404.html"

    contents = Path(filename).read_text()
    length = len(contents)

    response = (
        f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}".encode()
    )

    wfile = c.makefile(mode="wb", buffering=0)
    wfile.write(response)

    c.shutdown(socket.SHUT_RDWR)
    c.close()


def print_request(stream):
    http_request = []
    for line in rfile:
        if line == b"\r\n":
            c.shutdown(socket.SHUT_RDWR)
            c.close()
        else:
            http_request.append(line.decode().strip())

    print("Request:")
    pprint(http_request, indent=4)


if __name__ == "__main__":
    main()
