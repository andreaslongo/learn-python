# https://docs.python.org/3/howto/sockets.html

import socket
import io

def main():
    with socket.socket() as s:
        s.bind(("0.0.0.0", 7878))
        s.listen()
        while True:
            c, _ = s.accept()
            print("Connection established!")
            rfile = c.makefile(mode="rb", buffering=-1)
            for line in rfile:
                print(line)
                if line == b"\r\n":
                    print("close")
                    c.shutdown(socket.SHUT_RDWR)
                    c.close()


if __name__ == "__main__":
    main()
