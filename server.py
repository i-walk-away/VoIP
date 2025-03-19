"""
The Server is responsible for receiving and sending data to Clients
"""
import socket
#import threading

from src.utils.logger import logger
from src.services.config_service import ConfigService


class Server:
    """
    Server class
    """
    clients: set[tuple[str, int]] = set()

    def __init__(self, ip: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((ip, port))

        self.cfg = ConfigService('config/server_config.json')

        self.ip = self.cfg.get_value('IP')
        self.port = self.cfg.get_value('PORT')

    def start_server(self) -> None:
        """
        Initializes the Server on specified IP address and port
        """
        logger.info(f"Server is running and ready to accept data at {self.ip}:{self.port}")
        self._handle_clients()

    def _handle_clients(self) -> None:
        """
        Handles data from Clients in a separate thread. Recieves input audio streams from Clients
        and sends them to other Clients
        """
        while True:
            try:
                stream, address = self.socket.recvfrom(1024)
            except Exception as e:
                logger.error(
                    f"Error occured while receiving stream from client: {e}"
                )
                break

            if address not in self.clients:
                self.clients.add(address)
                logger.info(f"New client connected: {address}")

            for client_address in self.clients:
                self.send_stream_to_client(stream, client_address)

    def send_stream_to_client(self, stream, client_address: tuple[str, int]):
        """
        Tries to send audio stream data to Client.
        If exception occures, removes Client from clients.
        :param stream: stream
        :param client_address: Client's IP and PORT
        """
        try:
            self.socket.sendto(stream, client_address)
        except Exception as e:
            logger.info(f"Could not send stream to Client: {e}")
            self.remove_client(client_address)

    def remove_client(self, client_address: tuple[str, int]):
        """
        Use this method to remove a Client from clients.
        :param client_address: Tuple containing Client's IP and PORT.
        """
        if client_address in self.clients:
            self.clients.remove(client_address)
            logger.info(f"Disconnected client: {client_address}")


def main() -> None:  # pylint: disable=missing-function-docstring
    #FIXME: TEMP
    server = Server('127.0.0.1', 9999)
    server.start_server()


if __name__ == "__main__":
    main()
