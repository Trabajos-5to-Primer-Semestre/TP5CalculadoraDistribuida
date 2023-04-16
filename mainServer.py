import numexpr
import socket
import _thread
import threading

PORT = 6666


def receive_utf_msg(socket_connection):
    """
    Receive a message with Modified UTF
    :param socket_connection:  socket connection to use
    :return: The message that was received
    """
    length_of_message = int.from_bytes(socket_connection.recv(2), byteorder='big')
    msg = socket_connection.recv(length_of_message).decode("UTF-8")

    return msg


def send_msg_utf(socket_connection, msg):
    """
    Send a message using modified UTF
    :param socket_connection: socket connection to use
    :param msg: message to send
    """
    socket_connection.send(len(msg).to_bytes(2, byteorder='big'))
    socket_connection.send(msg)


def client_logic(socket_connection):
    with socket_connection:  # With the open connection
        thread_id = threading.current_thread().ident
        print(f"Thread ID {thread_id}: Connected by {addr}")

        while True:
            # Receive the socket message, specifying the max amount of data
            # The received data is then deserialized into a string
            data = receive_utf_msg(socket_connection)

            print(f"Thread ID {thread_id}: {data}")
            if data == 'no':
                print(f"Thread ID {thread_id}: Cerrando conexion...")
                break
            # Perform the calculations needed
            data = str(numexpr.evaluate(data.replace('^', '**'))).encode("UTF-8")
            # Serialize the data for sending back to the client
            send_msg_utf(socket_connection, data)


print('Inicializando socket')
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Binds an IP address and a port number to a socket instance and since the IP is empty it takes all ips
    s.bind(('', PORT))
    # Listens for connection attempts
    s.listen()

    while True:
        # Accepts the socket connection
        conn, addr = s.accept()
        # Lets a thread handle the specific socket connection
        _thread.start_new_thread(client_logic, (conn,))
