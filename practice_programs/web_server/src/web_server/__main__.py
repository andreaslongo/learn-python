# https://docs.python.org/3/howto/sockets.html

import socket
from pathlib import Path
from pprint import pprint
import time

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

    request_count = 0
    while request_count < 2:
        stream, _ = listener.accept()

        request_count += 1

        # We keep the API close to the threading module and don't use closures
        # (see below)
        pool.execute(target=handle_connection, args=[stream])

        # Closures alternative
        # We need defaults to reference loop variables when creating functions
        # inside loops. Otherwise, variables will bind only to the final loop
        # value.
        # pool.execute(lambda stream=stream: handle_connection(stream))

    print("Shutting down.")


def handle_connection(stream):
    # https://docs.python.org/3/library/io.html#module-io
    buf_reader = stream.makefile(mode="rb", buffering=-1)
    request_line = buf_reader.readline().decode().strip()

    match request_line:
        case "GET / HTTP/1.1":
            status_line, filename = ("HTTP/1.1 200 OK", "hello.html")
        case "GET /sleep HTTP/1.1":
            time.sleep(5)
            status_line, filename = ("HTTP/1.1 200 OK", "hello.html")
        case _:
            status_line, filename = ("HTTP/1.1 404 NOT FOUND", "404.html")

    contents = Path(filename).read_text()
    length = len(contents)
    response = f"{status_line}\r\nContent-Length: {length}\r\n\r\n{contents}".encode()

    writer = stream.makefile(mode="wb", buffering=0)
    writer.write(response)

    stream.close()


def print_request(stream):
    buf_reader = stream.makefile(mode="rb", buffering=-1)
    http_request = []
    for line in buf_reader:
        if line == b"\r\n":
            stream.shutdown(socket.SHUT_RDWR)
            stream.close()
        else:
            http_request.append(line.decode().strip())

    print("Request:")
    pprint(http_request, indent=4)


if __name__ == "__main__":
    main()
