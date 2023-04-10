import socket
import struct
import sys
import time

HOST = '127.0.0.1'
PORT = 123
TRUST_SERVER_ADDRESS = 'time.windows.com'
REQUEST = str.encode('\x23' + 47 * '\0')  # первый байти 0010 0011
TIME1970 = 2208988800
END = str.encode('end')


def description():
    print(f'''
    Данная программа - это сервер точного времени,
    который "врёт" на заданное количество времени.
    Сервер слушает порт 123 и запрашивает данные
    о времени у {TRUST_SERVER_ADDRESS}.
    Затем портит эти данные и отправляет своему клиенту.
    Количество времени на которое будет "лгать" сервер
    указано в файле "configuration.txt".
    ''')


def get_trust_time():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(REQUEST, (TRUST_SERVER_ADDRESS, PORT))
    message, address = client.recvfrom(1024)
    trust_time = struct.unpack("!12I", message)
    return list(trust_time)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print('Сервер начал работу')

    while True:
        conn, addr = s.accept()
        info = conn.recv(1024)
        if info == REQUEST:
            trust_time = get_trust_time()
            print("Trust time from {} :".format(TRUST_SERVER_ADDRESS), time.ctime(trust_time[10] + float(trust_time[11])/2**32 - TIME1970))

            try:
                with open('configuration.txt') as file:
                    trust_time[10] = trust_time[10] + int(file.readline())
            except (OSError, IOError) as e:
                print("File  'configuration.txt' wasn't opened.")
                conn.close()
                break
            except ValueError as e:
                print("Can't resolve the info from file 'configuration.txt'.")
                conn.close()
                break

            wrong_time = struct.pack("!12I", *trust_time)
            print("Wrong time :", time.ctime(trust_time[10] + float(trust_time[11])/2**32 - TIME1970))
            conn.send(wrong_time)

        conn.close()
        if info == END:
            print('Завершение работы сервера')
            break

    s.close()


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        if args[1] == '-h' or args[1] == '--help':
            description()
        else:
            print("Неправильный ввод")
    elif len(args) == 1:
        main()
    else:
        print("Неправильный ввод")
