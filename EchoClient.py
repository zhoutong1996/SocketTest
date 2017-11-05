import socket
import argparse


def echo_client(port,msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('localhost', port)
    print "Connectting to  %s port %s" % server_address
    sock.connect(server_address)

    #  send data
    try:
        #  send data
        message = msg
        print "sengding %s"%message
        sock.sendall(message)
        # look for response
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
            print"received: %s"%data
    except socket.error, e:
        print"socket error:%s"%str(e)
    except Exception,e:
        print"other exception:%s"%str(e)
    finally:
        print"closing connection to the server"
        sock.close()






if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port',action = "store", dest='port', type=int, required=True)
    parser.add_argument('--msg', action="store", dest='msg', type=str, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    msg = given_args.msg
    echo_client(port, msg)