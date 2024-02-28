import pickle
import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 27000

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def executeTask(task):
    function, args = task
    if function == add:
        return add(*args)
    elif function == subtract:
        return subtract(*args)
    else:
        raise ValueError("Unsupported function: ".format(function))
 
def main():
    ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ServerSocket.bind((SERVER_HOST, SERVER_PORT))
    ServerSocket.listen()
    print("Worker node waiting for tasks...")
    try:
        connection, addr = ServerSocket.accept()
        print("Connected by: ", addr)
        with connection:
            while True:
                # Recieve pickled task from client
                data = connection.recv(10000)
                if not data:
                    break
                task = pickle.loads(data)
                # Execute task
                result = executeTask(task)
                # Send result back to client
                connection.sendall(pickle.dumps(result))
    except (socket.error, socket.timeout) as error:
        print(f"Error: {error}")
        ServerSocket.close()

main()
