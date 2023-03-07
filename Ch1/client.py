# Client.py
import socket
import sys
from threading import Thread

server_address = ('127.0.0.1', 5000)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)


math = ""
reply = ""
YES = 0

def thread_input():
    global math 
    math = input("Masukkan perhitungan matematika: ")

def thread_recv():
    global reply 
    reply = client_socket.recv(1024).decode()


if __name__ == "__main__":
    thread1 = Thread(target = thread_input)
    thread2 = Thread(target = thread_recv)

    thread1.start()
    thread2.start()

    while True:
        if math:
            # Input sudah masuk
            # mengirim data ke server
            msg = math

            # kirim data ke server
            client_socket.send(msg.encode())

            # math dikembalikan menjadi false
            math = ""
            thread1.join()
            YES = 1

        if reply:
            reply = reply.replace("b", "")
            reply = reply.replace("'", "")
            if YES:
                sys.stdout.write("Pesan terkirim ke client lain. Isi pesan: " + str(reply))
                YES = 0
            else:
                print("-> " + str(reply))
            client_socket.send(reply.encode())
            thread1.join()
            thread2.join()
            break

        # #Keyboard interrupt
        # try:
        #     thread1.join()
        #     thread2.join()
        # except KeyboardInterrupt:
        #     print("Keyboard interrupt")
        #     client_socket.close()
        #     sys.exit(0)

    client_socket.close()
    sys.exit(0)