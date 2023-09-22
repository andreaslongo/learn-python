# https://docs.python.org/3/howto/sockets.html

import socket
import io

def main():
    with socket.socket() as s:
        s.bind(("0.0.0.0", 7878))
        s.listen()
        while True:
            s.accept()
            buffer = s.makefile()
            s.recv_into(buffer)
            print("Connection established!")


if __name__ == "__main__":
    main()
