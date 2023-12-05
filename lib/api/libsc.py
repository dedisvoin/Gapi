
from typing import Iterable, Tuple
from ast import literal_eval
from time import sleep
import socket


LOCALHOST = "localhost"
LOCALPORT = 8000

def StringToList(string_: str) -> list:
    '''Converting liststring object to list object'''
    return literal_eval(string_)

def ListToString(list_: list) -> str:
    '''Converting string object to list object'''
    return str(list_)

# ! NEW METHOD!!!
def GetMyHost() -> str:
    return socket.gethostbyname(socket.gethostname())


def Packing(data_: Iterable, packet_name_: str) -> bytes:
    '''Packing any information types to bytecode'''
    pack = [packet_name_, data_]
    convert_data = ListToString(pack).encode()
    return convert_data

def Unpacking(data_: bytes) -> list:
    '''Decoding any information'''
    try:
        convert_data = StringToList(data_.decode())
        return convert_data
    except:
        return [None, None]


def GetPacketWithName(packet: bytes, name_: str):
    '''Get packet with here name'''
    
    packet_list = Unpacking(packet)
    if packet_list[0] == name_:
        return packet_list[1]
    else:
        None



class Server:
    def __init__(
        self,
        port_: int = LOCALPORT, host_: str = LOCALHOST,
        name_: str = "Default Server",
        max_client_: int = 1,
    ) -> None:
        # ? Created default server with writed properies
        self._port = port_
        self._host = host_
        self._name = name_
        self._max_client = max_client_
        
        self._client_con = False
        self._end_client_data = [None,None]
        
        self._client_decon = False
        self._client_decon_data = [None,None]

        # ? list of connected clients
        self._clients: Tuple[Tuple[socket.socket, int],...] = []

        self.init()
    
    @property
    def max_clients_connected(self) -> bool:
        '''return maxed clients value '''
        return len(self._clients)<self._max_client
    
    @property
    def client_connect_event(self) -> bool:
        return self._client_con
    
    @property
    def client_deconnect_event(self) -> bool:
        return self._client_decon

    def init(self) -> None:
        # ? Construct default server
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._server.bind((self._host, self._port))
        self._server.setblocking(0)
        self._server.listen(5)
        
        
        print(f'Server to {self._port=} {self._host=} started!')
        print(f'Wait {self._max_client} connections...')

    def wait_con(self, sleep_sec_: float):
        sleep(sleep_sec_)

        if len(self._clients) < self._max_client:
            try:
                
                client, addr = self._server.accept()
                client.setblocking(0)
                self._clients.append([client, addr])
                
                self._client_con = True
                self._end_client_data = [client, addr]
                
                print(f"Client {addr} connected!")
                
                
            except:
                self._client_con = False
                self._end_client_data = [None, None]
        else:
            self._client_con = False
            self._end_client_data = [None, None]

    def send_packet_all_clients(self, packet_: bytes, sleep_sec_: float = 0):
        sleep(sleep_sec_)
        for index in range(len( self._clients )):
            try:
                self._clients[index][0].send(packet_)
                self._client_decon = False
                self._client_decon_data = [None, None]
            except:
                print(f'Client {self._clients[index][1]} closed!')
                self._client_decon = True
                self._client_decon_data = self._clients[index]
                self._clients[index][0].close()
                
                del self._clients[index]
                print(f'{len(self._clients)}/{self._max_client} connected.')
                break
            
    def recv_packets_all_clients(self, buff_size_: int = 2048, sleep_sec_: float = 0, name_: str = 'None'):
        sleep(sleep_sec_)
        all_clients_packets = []
        for index in range(len(self._clients)):
                try:
                    packet = self._clients[index][0].recv(buff_size_)

                    if GetPacketWithName(packet, name_) != None:
                        pack = [self._clients[index][1], GetPacketWithName(packet, name_)]
                        all_clients_packets.append(pack)
                except:
                    ...

        return all_clients_packets
                
        
                


class Client:
    def __init__(self, port_: int = LOCALPORT, host_: str = LOCALHOST) -> "Client":
        self._port = port_
        self._host = host_

        self.init()
        
    def init(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._client.connect((self._host, self._port))
        
        print(f"Connected to {self._port=} {self._host}")
        
    def recv_packet(self, buff_size_: int = 2048,sleep_sec_: float = 0) -> bytes:
        sleep(sleep_sec_)
        data_ = self._client.recv(buff_size_)
        return data_
    
    def send_packet(self, packet_, sleep_sec_: float = 0):
        sleep(sleep_sec_)
        try:
            self._client.send(packet_)
        except:...
        
