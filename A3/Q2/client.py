import pickle
import socket
 
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

def sendTask(task):
    try:
        # Create socket object
        ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server
        ClientSocket.connect((SERVER_HOST, SERVER_PORT))
        # Pickle and send the object
        ClientSocket.sendall(pickle.dumps(task))
        # Recieve the result from server
        data = ClientSocket.recv(10000)
        result = pickle.loads(data)
        return result
    except(socket.error, socket.timeout) as error:
        print(f"Error: {error}")
        return None
    finally:
        ClientSocket.close()

# A task
def add(x, y):
    return x + y

# A task
def subtract(x, y):
    return x - y

def main():
    task = (subtract, (8,5)) # Function and args to be executed
    result = sendTask(task)
    print("Result: ", result)

main()
