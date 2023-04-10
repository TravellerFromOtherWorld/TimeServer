import socket
import struct
import time

HOST = '127.0.0.1'
PORT = 123
REQUEST = str.encode('\x23' + 47 * '\0')
TIME1970 = 2208988800
END = str.encode('end')


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(END)
    while True:
        buf = s.recv(1024)
        try:
            res = struct.unpack('!12I', buf)
            print('Полученное время:')
            print(time.ctime(res[10] + float(res[11])/2**32 - TIME1970))
        except struct.error:
            pass
        if len(buf) == 0:
            break

    s.close()


if __name__ == "__main__":
    main()
