import socket
import pickle
import os

#Define the server address and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

SAVE_DIRECTORY='./recieved-files/'
 
# Save the recieved file
def save_file(fileData, filename):
    with open(os.path.join(SAVE_DIRECTORY, filename), 'wb') as f:
        f.write(fileData)
    print(f"File '{filename}' saved succesfully!")

def main():
    # Create Socket
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind Socket
    ServerSocket.bind((SERVER_HOST, SERVER_PORT))
    # Listen
    ServerSocket.listen(1)
    print("Server listening for connection...")

    while True:
        # Accept
        ClientSocket, ClientAddress = ServerSocket.accept()
        print(f"Connection established with {ClientAddress}")

        # Recieve pickled file object from client
        fileData = ClientSocket.recv(4096)
        # Unpickle the file object
        try:
            filename, fileContent = pickle.loads(fileData)
        except pickle.UnpicklingError as error:
            print("Error while unpickling: ", error)
            continue

        # Save the file
        save_file(fileContent, filename)

        # Close client connection
        ClientSocket.close()

main()