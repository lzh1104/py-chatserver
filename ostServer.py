__author__ = 'Swoosh'
import select
import socket
import ostClientConnection
import ostCallbacks
import ostPacket
import ostClient
import ostConst
import ostClientManager
import ostPacketBuilder
import ostPacketParser
import random

class ostServer:

    _srv_socket = 0
    _endpoint_addr = ""
    _endpoint_port = 0
    _connected_clients = None
    _client_id_counter = 0

    _client_manager = ostClientManager.ostClientManager()
    _p_builder = ostPacketBuilder.ostPacketBuilder()
    _p_parser = ostPacketParser.ostPacketparser()

    #callbacks
    _cb_connected_client = None

    def __init__(self,endpoint_addr,endpoint_port):
        # create normal INET socket for listening to incoming connections
        self._srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # we want a nonblocking connection, so we can process everything at once
        self._srv_socket.setblocking(0)
        self._srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # set internal endpoint data
        self._endpoint_addr = endpoint_addr
        self._endpoint_port = endpoint_port
        #create dict
        self._connected_clients = dict()
        random.seed(1337)

    def bindServer(self):
        # bind to endpoint

        self._srv_socket.bind((self._endpoint_addr, self._endpoint_port))
        print("ostServer.bindServer : Bound to endpoint " + self._endpoint_addr, ":" + str(self._endpoint_port))

    def startServerListen(self):
        # start listening for incoming connections, limit queue size to 20
        self._srv_socket.listen(20)


    def onlineClientCount(self):
        return len(self._connected_clients)


    def processConnections(self):
        # first, we check if there's a new connection pending.
        fds_in, fds_out, fds_err = select.select([self._srv_socket], [], [], 0)
        # check if result of select is our server socket
        if (self._srv_socket in fds_in):
            new_client, client_addr = self._srv_socket.accept()
            new_client.setblocking(False)
            new_client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)



            print("ostServer.processConnections : New incomming connection! Client=", client_addr)
            # create new client
            nc = ostClient.ostClient(new_client)

            # add client to list of connected clients
            self._connected_clients[new_client] = nc
            #call callback event
            if self._cb_connected_client is not None:
                self._cb_connected_client(nc)

        # now process all connected clients
        connected_fds = []
        for con in self._connected_clients:
            connected_fds.append(self._connected_clients[con].getSocket())

        if len(connected_fds) > 0:
            fds_in, fds_out, fds_err = select.select(connected_fds, connected_fds, connected_fds, 0)
            # process data individually
            # recv
            for fd_in in fds_in:
                if fd_in in self._connected_clients:
                    self.__recvClient(fd_in, self._connected_clients[fd_in])
            #send
            for fd_out in fds_out:
                if fd_out in self._connected_clients:
                    self.__sendClient(fd_out, self._connected_clients[fd_out])


        #process packet tasks
        for client in self._connected_clients.values():
            self.processPackets(client)

    def processPackets(self,client : ostClient.ostClient):



        #cycle through all existing packets that we have in queue
        while (client.hasRecvPacket()):
            p = client.getRecvPacket()
            opcode = p.getOpcode()
            print("recv packet, p=", p.toString())
            if (opcode == ostConst.OST_OPCODE_MSG_C2S_HANDSHAKE_RESPONSE):
                #get client version
                client_version,nickname = self._p_parser.parsePacket_MSG_C2S_HANDSHAKE_RESPONSE(p)
                #increment counter id
                self._client_id_counter += 1
                #provide id to client
                client.setId(self._client_id_counter)
                client.setVersion(client_version)
                client.setNickname(nickname)
                 #set client state to authed
                client.setState(ostClientConnection.ostClientConnectionState.ostAuthed)
                print("ostServer : Client is now authed. client=" + client.toString())
                #add client to clientmanager
                self._client_manager.addClient(client)
                #send handshake state message to newly authed client
                client.addSendPacket(self._p_builder.buildPacket_MSG_S2C_HANDSHAKE_STATE(ostConst.OST_AUTH_HANDSHAKE_OKAY))
                client.addSendPacket((self._p_builder.buildPacket_MSG_S2C_ONLINE_LIST(self._client_manager.getClients())))
                #send message to all connected clients
                self._client_manager.broadcastPacket(self._p_builder.buildPacket_MSG_S2C_NEWCLIENT_BROADCAST(client.getId(),client.getNickname()))


            else:
                if (opcode == ostConst.OST_OPCODE_MSG_C2S_CHAT_MESSAGE):
                    print("msg recv!")
                    #check if client is even authed
                        #if (client.getState() == ostClientConnection.ostClientConnectionState.ostAuthed):
                    if (True):
                        chat_msg_len,chat_msg = self._p_parser.parsePacket_MSG_MSG_C2S_CHAT_MESSAGE(p)
                        print("Recv chat, recv_client=", client.toString(), ", msg=", chat_msg)
                        self._client_manager.broadcastPacket(self._p_builder.buildPacket_MSG_S2C_CHAT_MESSAGE(client.getId(),chat_msg))
                    else:
                        #an hero
                        client.terminateConnection()
                        del self._connected_clients[client]
                        print("ostServer : Client banhammered. client=" + client.toString())


    def __recvClient(self,socket : socket, con : ostClient.ostClient):

        try:
            recv_buf_header = socket.recv(5)
            #print("recv header: ",recv_buf_header)
            if (recv_buf_header):
                if len(recv_buf_header) >= 5:
                    recv_buf_header_bytes = bytearray(recv_buf_header)
                    opcode = recv_buf_header_bytes[0]
                    pck_len = (recv_buf_header_bytes[4] << 24) | (recv_buf_header_bytes[3] << 16) | (recv_buf_header_bytes[2] << 8) | (recv_buf_header_bytes[1])
                    if (pck_len > 65535):
                        print("Recv length in header over 65kb, goodbye. socket=", str(socket))
                        con.terminateConnection()
                        del self._connected_clients[socket]
                        return

                    recv_buf_payload = socket.recv(pck_len)

                    new_packet = ostPacket.ostPacket()
                    new_packet.setOpcode(opcode)
                    for b in recv_buf_payload:
                        new_packet.writeByte(b)

                    new_packet.resetPivot()
                    con.addRecvPacket(new_packet)

                    #print("recv header: ",recv_buf_header, " opcode=", opcode, ", len=", pck_len, ", payload=",recv_buf_payload)
                else:
                    print("Recv less than 5 bytes, goodbye. socket=", str(socket))
                    con.terminateConnection()
                    del self._connected_clients[socket]

            else:
                # disconnect, since socket just an heroed
                del self._connected_clients[socket]
                con.terminateConnection()
                print("Client disconnected! client=", con.toString())

        except:
            con.terminateConnection()
            del self._connected_clients[socket]
            print("Client disconnected! client=", con.toString())




    def __sendClient(self,socket : socket, con : ostClientConnection.ostClientConnection):

        if (con.hasSendPacket()):
            p = con.getSendPacket()

            ba = p.toByteArray()
            socket.send(ba)
            #   print("Sent a packet, p=", ba)




    def setCallbackClientConnect(self,cb_method):
        self._cb_connected_client = cb_method