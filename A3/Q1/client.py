import socket
import pickle

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

def pickle_file(file):
    # Read the file and pickle it 
    try:
        with open(file, 'rb') as f:
            fileContent = f.read()
        return(file, fileContent)
    except IOError as error:
        print("Error reading file", error)
        return None
    
def main():
    # Ask user for input
    filePath = input("Enter the path of the file to transfer: ")
    
    # Pickle the file
    fileData = pickle_file(filePath)
    if not fileData:
        return
    
    # Create a socket for client
    ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ClientSocket.connect((SERVER_HOST, SERVER_PORT))

        ClientSocket.send(pickle.dumps(fileData))
        print("File sent successfully!")
    except Exception as error:
        print("Error: ", error)
    finally:
        ClientSocket.close()

main()