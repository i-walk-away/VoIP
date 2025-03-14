"""
The Server is responsible for receiving and sending data to Clients.
Currently it's only capable of handling audio streams.
Other types of data are to be implemented in the future (messages, images, Plague Inc files)
"""
import socket
import threading

from src.utils.logger import logger

# FIXME: Temp
IP = input("IP ADDRESS: ")
PORT = int(input("PORT: "))


class Server:
    """
    Server class
    """
    clients: list[socket.socket] = []

    def __init__(self, ip: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(5)

        self.ip = ip
        self.port = port

    def start_server(self) -> None:
        """
        Initializes the Server on specified IP address and port
        """
        logger.info(f"Server is running and ready to accept data at {self.ip}:{self.port}")

        while True:
            client, _ = self.socket.accept()

            self.clients.append(client)

            thread = threading.Thread(
                target=self._handle_client,
                args=(client, )
            )
            thread.start()

    def _handle_client(self, client: socket.socket) -> None:
        """
        Handles data from Clients in a separate thread. Recieves input audio streams from Clients
        and sends them to other Clients
        """
        while True:
            try:
                stream = client.recv(1024)
            except Exception as e:
                logger.error(
                    f"Error occured while receiving stream from client {client.getsockname()}: {e}"
                )
                break

            for receiver in self.clients:                       # This makes sure that the sender of
                if receiver is not client:                      # an audio stream does not receive
                    receiver.send(stream)                       # his own voice back from the Server

        self.clients.remove(client)
        client.close()


def main() -> None:  # pylint: disable=missing-function-docstring
    server = Server(IP, PORT)
    server.start_server()


if __name__ == "__main__":
    main()
