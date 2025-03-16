"""
The Client object connects to the Server and exchanges data with it
"""
import socket

from pyaudio import PyAudio, paInt16, Stream

from src.utils.logger import logger


# FIXME: Temp
FORMAT: int = paInt16
CHANNELS: int = 1
SAMPLING_RATE: int = 4000
FRAMES_PER_BUFFER: int = 256

IP = input("IP ADDRESS: ")
PORT = int(input("PORT: "))


class Client:
    """
    Client class
    """
    def __init__(self):
        self.audio = PyAudio()

        # Input and output audio stream initialisation
        self.stream_input = self.get_input_stream()
        self.stream_output = self.get_output_stream()

        try:
            self._connect_to_server(IP, PORT)
        except Exception as e:
            logger.error(f"Failed to connect to server '{IP}:{PORT}': {e}")

    def get_input_stream(self) -> Stream:
        """
        Returns the input Stream
        """
        return self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLING_RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

    def get_output_stream(self) -> Stream:
        """
        Returns the output Stream
        """
        return self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLING_RATE,
            output=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
        )

    def _connect_to_server(self, ip: str = "127.0.0.1", port: int = 9999) -> None:
        """
        Connects to the Server on specified IP address and port
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)

        self.socket.connect((ip, port))
        logger.info(f"Successfully connected to '{ip}:{port}'")

        self._start_loop()

    def _start_loop(self) -> None:
        """
        Main loop in which the Client sends input stream data to the Server
        and handles output stream data from it.
        """
        while True:
            self._send_input_stream_to_server()
            data = self.socket.recv(1024)

            if data:
                self._handle_stream_from_server(data)

    def _send_input_stream_to_server(self) -> None:
        """
        Sends an audio input stream to the Server in bytes format
        """
        input_data = self._get_microphone_stream()
        self.socket.send(input_data)

    def _get_microphone_stream(self) -> bytes:
        """
        Gets data from the audio input stream
        """
        return self.stream_input.read(FRAMES_PER_BUFFER, exception_on_overflow=False)

    def _handle_stream_from_server(self, stream: bytes) -> None:
        """
        Handles the output stream data from the Server
        """
        self.stream_output.write(stream)


client = Client()
