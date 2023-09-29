# https://docs.python.org/3/howto/sockets.html

import socket
from pathlib import Path
from pprint import pprint
import time



def main():
    # We set socket.SO_REUSEADDR to avoid: "OSError: [Errno 98] Address already
    # in use" after ending with CTRL+C.
    with socket.socket(socket.SO_REUSEADDR) as s:
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
    elif request_line == 'GET /sleep HTTP/1.1':
        time.sleep(5)
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
