import socket
import argparse


def echo_server(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', port)
    print "Starting up echo server on %s port %s" % server_address

    sock.bind(server_address)
    sock.listen(5)

    while True:
        print "Waiting to receive message from client"
        client, address = sock.accept()
        data = client.recv(2048)
        if data:
            print"data:%s" % data
            client.send(data)
            print"sent %s bytes back to %s" % (data, address)
        client.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port',action = "store", dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    echo_server(port)