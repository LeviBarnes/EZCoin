import socket
import pickle

default_port = 10103
timeout = 10

class EasyCoinManifest:
    def __init__(self, obj):
        self.kind = type(obj)
        self.sz = len(pickle.dumps(obj))

def newClientSocket(port=None):
    """
    EZCoinSocket.newClientSocket(port=default_port) -> socket

    Opens and returns a new client socket for sending messages
    """
    #if port==None:
    #    port = default_port
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', port)
    print('connecting to {} port {}'.format(*server_address))
    sock.settimeout(timeout)
    try:
        sock.connect(server_address)
    except:
        print("No server on port " + str(port))
        return None
    return sock

def sendMessage(obj, clientSocket):
    """
    sendMessage(obj, clientSocket)

    Sends a pickle-able object over the given socket.
    """
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

def newServerSocket(port=None):
    """
    newServerSocket(port=default_port) -> socket

    Opens and returns a new server socket
    """
    if port==None:
        port = default_port
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = ('localhost', port)
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)

    # Listen for incoming connections
    sock.listen(1)
    return sock


def recvNewObject(serverSocket):
    """
    recvNewObject(socket)

    Receives a new object over the given socket (assumed listening)
    The server first expects a manifest which consists of a type and size
    On receipt of a valid manifest, sends ACK_MFST. Then, receives and
    pickle loads the object and returns
    """
    # Wait for a connection
    serverSocket.settimeout(timeout)
    print('waiting for a connection on socket ' + str(serverSocket.getsockname()))
    try:
        connection, client_address = serverSocket.accept()
    except:
        print("No connection.")
        serverSocket.settimeout(None)
        return None
    all_data = b""
    try:
        print('connection from', client_address)

        manifest_d = connection.recv(100)
        manifest = pickle.loads(manifest_d)
        expected = manifest.sz
        print ("Expecting a " +str(manifest.kind) + " of size " + str(expected))
    except:
        raise RuntimeError("Receipt of mainfest failed.")
        serverSocket.settimeout(None)
        return None
    try:

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
        raise RuntimeError("Receipt of object failed.")
        serverSocket.settimeout(None)
        return None
    finally:
        print ("received " + str(data_in) + " characters. Acknowledging...")
        connection.send(b"ACK_MMSG")
        print("Unpickling block ")
        newBlock = pickle.loads(all_data)
        connection.close()
        serverSocket.settimeout(None)
    return newBlock




