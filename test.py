import socket
import argparse
from binascii import hexlify

class SodcketFunc:
    def __init__(self):
        pass

    def get_machine_info(self):
        host_name = socket.gethostname()
        ip_addr = socket.gethostbyname(host_name)
        return {'host_name': host_name, 'ip_addr': ip_addr}

    def get_remote_host(self):
        remote_host = 'www.python.org'
        try:
            return ('IP address of %s: %s'%(remote_host, socket.gethostbyname(remote_host)))
        except socket.error, err_msg:
            return ('%s:%s'%(remote_host,err_msg))

    def convert_ipv4_address(self,ip_addr):
        packed_ip = socket.inet_aton(ip_addr)
        print type(packed_ip)
        unpacked_ip = socket.inet_ntoa(packed_ip)
        return ('IP address:%s => Packed ip:%s => Unpacked ip:%s'%(ip_addr, hexlify(packed_ip), unpacked_ip))

    def find_server_name(self,port=[80,25]):
        protocol_name = 'tcp'
        for port in port:
            print port, socket.getservbyport(port,protocol_name)
        print '53', socket.getservbyport(53, 'udp')

    def convert_integer(self,data=1234):
        """convert data from Network byte order to Host byte order ,or on the opposite"""
        # 32-bit
        print 'Original: %s => Long host byte order: %s,Network byte order: %s'\
               %(data, socket.ntohl(data), socket.htonl(data))
        # 16-bit
        print 'Original: %s => Short host byte order: %s,Network byte order: %s'\
               %(data, socket.ntohs(data), socket.htons(data))

    def socket_timeout_test(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket instance
        print 'Default socket timeout:%s'%s.gettimeout()
        s.settimeout(100)
        print 'Socket timeout after setting:%s' % s.gettimeout()

    def reuse_socket_addr(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get old state of the SO_REUSEADDRA option
        old_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        print "Old sock state: %s"%old_state

        # Enable the SO_REUSEADDR option
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        new_state = sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
        print "New sock state: %s"%new_state

        local_port = 8282

        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(('', local_port))
        srv.listen(1)
        print("Listening on port: %s"%local_port)
        while(True):
            try:
                connection, addr = srv.accept()
                print connection
                print "Connected by %s:%s"%(addr[0], addr[1])
            except KeyboardInterrupt:
                break
            except socket.error, msg:
                print msg

    def echo_server(self,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('localhost', port)
        print "Starting up echo server on %s port %s"%server_address

        sock.bind(server_address)
        sock.listen(5)

        while True:
            print "Waiting to receive message from client"
            client, address = sock.accept()
            data = client.recv(2048)
            if data:
                print"data:%s"%data
                client.send(data)
                print"sent %s bytes back to %s"%(data, address)
            client.close()



if __name__ == '__main__':

    #  =============================================for echo_server()
    parser = argparse.ArgumentParser(description='Socket Server Example')
    parser.add_argument('--port',action = "store", dest='port', type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    #  ==============================================================
    info = SodcketFunc()
    info.echo_server(port)
