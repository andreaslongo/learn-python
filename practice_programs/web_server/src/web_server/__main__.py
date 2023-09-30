# https://docs.python.org/3/howto/sockets.html

import socket
from pathlib import Path
from pprint import pprint
import time
from threading import Thread

from lib import ThreadPool


def main():
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # We set socket flag "SO_REUSEADDR", in order to prevent
    # "OSError: [Errno 98] Address already in use".
    # https://docs.python.org/3/library/socket.html#example
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("0.0.0.0", 7878))
    listener.listen()

    pool = ThreadPool(4)

    while True:
        stream, _ = listener.accept()
        print("Connection established!")

        # Thread(target=handle_connection, args=[stream]).start()
        pool.execute(lambda: handle_connection(stream))

        # This leads to linter error:
        # B023 Function definition does not bind loop variable `stream`
        # Thread(target=lambda: handle_connection(stream)).start()


def handle_connection(stream):
    # https://docs.python.org/3/library/io.html#module-io
    rfile = stream.makefile(mode="rb", buffering=-1)
    request_line = rfile.readline().decode().strip()

    match request_line:
        case "GET / HTTP/1.1":
            status_line = "HTTP/1.1 200 OK"
            filename = "hello.html"
        case "GET /sleep HTTP/1.1":
            status_line = "HTTP/1.1 200 OK"
            filename = "hello.html"
            time.sleep(5)
        case _:
            status_line = "HTTP/1.1 404 NOT FOUND"
            filename = "404.html"

    contents = Path(filename).read_text()
    length = len(contents)

    response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}".encode()

    wfile = stream.makefile(mode="wb", buffering=0)
    wfile.write(response)

    stream.close()


def print_request(stream):
    rfile = stream.makefile(mode="rb", buffering=-1)
    http_request = []
    for line in rfile:
        if line == b"\r\n":
            stream.shutdown(socket.SHUT_RDWR)
            stream.close()
        else:
            http_request.append(line.decode().strip())

    print("Request:")
    pprint(http_request, indent=4)


if __name__ == "__main__":
    main()
