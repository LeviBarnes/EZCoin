import socket
import pickle

class EasyCoinManifest:
    def __init__(self, obj):
        self.kind = type(obj)
        self.sz = len(pickle.dumps(obj))

def newClientSocket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', 10000)
    print('connecting to {} port {}'.format(*server_address))
    sock.connect(server_address)
    return sock

def sendMessage(obj, clientSocket):
    try:
        # Send manifest
        message = pickle.dumps(EasyCoinManifest(obj))
        #print('sending {!r}',format(message))
        clientSocket.sendall(message)

        # Recv acknowledgement
        data = clientSocket.recv(8)
        if data != b"ACK_MFST":
            raise RuntimeError("Server did not acknowledge manifest")
            return -1
        # Send data
        message = pickle.dumps(obj)
        #print('sending {!r}'.format(message))
        clientSocket.sendall(message)

        data = clientSocket.recv(8)
        if data != b"ACK_MMSG":
            raise RuntimeError("Server did not acknowledge message")
            return -1
        return 0
    except:
        raise RuntimeError("sendMessage failed")
        return -1

def openServerSocket():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', 10000)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    return sock

def recvNewBlock(serverSocket):
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = serverSocket.accept()
    all_data = b""
    try:
        print('connection from', client_address)

        manifest_d = connection.recv(100)
        manifest = pickle.loads(manifest_d)
        expected = manifest.sz
        print ("Expecting a " +str(manifest.kind) + " of size " + str(expected))

        connection.send(b"ACK_MFST")
        data_in = 0
        # Receive the data in small chunks and retransmit it
        while data_in < expected:
            data = connection.recv(16)
            #print('received {!r}'.format(data))
            if data:
                #print('sending data back to the client')
                #connection.sendall(data)
                pass
            else:
                #print('no data from', client_address)
                break
            all_data = all_data + data
            data_in = data_in + len(data)
    except:
        raise RuntimeError("Receipt of block failed.")
        return None
    finally:
        print ("received " + str(data_in) + " characters. Acknowledging...")
        connection.send(b"ACK_MMSG")
        print("Unpickling block ")
        newBlock = pickle.loads(all_data)
        connection.close()
    return newBlock




