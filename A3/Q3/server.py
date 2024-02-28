import pickle
import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

clients = []  # List to store client sockets
lock = threading.Lock()  # Lock for safety

def broadcast(message, senderSocket):
    with lock:
        for ClientSocket in clients:
            if ClientSocket != senderSocket:
                try:
                    ClientSocket.send(message)
                except Exception as error:
                    print(f"Error broadcasting message to client: {error}")

def handleClient(ClientSocket, ClientAddress):
    # Add a client to the list
    with lock:
        clients.append(ClientSocket)

    print(f"New connection from {ClientAddress}")

    try:
        while True:
            # Receive message from client
            message = ClientSocket.recv(10000)
            # Check if message is empty
            if not message:
                break
            # Broadcast the message to all clients
            broadcast(message, ClientSocket)
    except Exception as error:
        print(f"Error broadcasting message to client: {error}")
    finally:
        ClientSocket.close()
        with lock:
            clients.remove(ClientSocket)
        print(f"Connection closed by {ClientAddress}")

def main():
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.bind((SERVER_HOST, SERVER_PORT))
    ServerSocket.listen()

    print(f"Server is listening for connections...")

    try:
        while True:
            # Accept incoming connections and handle them in separate threads
            ClientSocket, ClientAddress = ServerSocket.accept()
            ClientThread = threading.Thread(target=handleClient, args=(ClientSocket, ClientAddress))
            ClientThread.start()
    except KeyboardInterrupt:
        # Close the server socket when KeyboardInterrupt is received ---> Ctrl+C
        print("Shutting down the server")
        ServerSocket.close()

main()
