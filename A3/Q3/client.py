import pickle
import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

def recvMessage(ClientSocket):
    try:
        while True:
            # Recieve and print messages from the server
            message = ClientSocket.recv(10000)
            print("\nRecieved message from: ",pickle.loads(message))
            print("Enter a message from: ", end="", flush=True)
    except Exception as error:
        print(f"Error recieving message: {error}")

def sendMessage(ClientSocket):
    try:
        while True:
            # Get input from user and send it to server
            message = input("Enter a message: ")
            ClientSocket.send(pickle.dumps(message))
    except Exception as error:
        print(f"Error sending message: {error}")
    finally:
        ClientSocket.close()

def main():
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ClientSocket.connect((SERVER_HOST, SERVER_PORT))

    recvThread = threading.Thread(target=recvMessage, args=(ClientSocket,))
    recvThread.start()

    sendThread = threading.Thread(target=sendMessage, args=(ClientSocket,))
    sendThread.start()

main()