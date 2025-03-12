"""
Сервер, отвечающий за получение и отправку аудио-потоков клиентам
"""
import socket
import threading

from src.utils.logger import logger

# FIXME: Temp
IP = input("IP ADDRESS: ")
PORT = int(input("PORT: "))


class Server:
    clients: list[socket.socket] = []

    def __init__(self, ip: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(5)

        self.ip = ip
        self.port = port

    def start_server(self) -> None:
        """
        Запуск сервера для обработки запросов с клиента
        """
        logger.info(f"Server is running and ready to accept data at {self.ip}:{self.port}")

        while True:
            client, address = self.socket.accept()

            self.clients.append(client)

            thread = threading.Thread(
                target=self._handle_client,
                args=(client, )
            )
            thread.start()

    def _handle_client(self, client: socket.socket) -> None:
        """
        Обработка клиента в отдельном потоке. Отвечает за получение его аудио-потока
        и отправку аудио других клиентов
        """
        while True:
            try:
                stream = client.recv(1024)
            except Exception as e:
                logger.error(
                    f"Error occured while receiving stream from client {client.getsockname()}: {e}"
                )
                break

            for receiver in self.clients:
                if receiver is not client:
                    receiver.send(stream)

        self.clients.remove(client)
        client.close()


def main() -> None:
    server = Server(IP, PORT)
    server.start_server()


if __name__ == "__main__":
    main()
