# https://docs.python.org/3/howto/sockets.html

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

import socket
import io
from pprint import pprint

def main():
    with socket.socket() as s:
        s.bind(("0.0.0.0", 7878))
        s.listen()
        while True:
            c, _ = s.accept()
            print("Connection established!")
            rfile = c.makefile(mode="rb", buffering=-1)
            http_request = []
            for line in rfile:
                if line == b"\r\n":
                    c.shutdown(socket.SHUT_RDWR)
                    c.close()
                else:
                    http_request.append(line)
            print("Request:")
            pprint(http_request, indent=4)


if __name__ == "__main__":
    main()
