import socket

PORT = 6666
HOST = "127.0.0.1"


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


# Creates socket class element specifying the address family and socket type
# Socket_stream = TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connects to the socket
    s.connect((HOST, PORT))

    run = 'yes'

    while run != 'no':

        expr = input('Ingrese la expresion matematica a evaluar: \n')

        # Serialize the user input to be sent into bytes, and then we send it
        expr = bytes(expr, encoding='UTF-8')
        send_msg_utf(s, expr)

        # The data is received and deserialized
        data = receive_utf_msg(s)

        print(f'El resultado es: {data}')

        run = input('Desea realizar otro calculo? [si/no]: \n')
        if run == 'no':
            send_msg_utf(s, bytes(run, encoding="UTF8"))
            print("Cerrando conexion con el servidor...")
