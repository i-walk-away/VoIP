"""
The Client object connects to the Server and exchanges data with it
"""
import socket

from pyaudio import PyAudio, paInt16, Stream

from src.utils.logger import logger
from src.services.config_service import ConfigService


# FIXME: Temp
FORMAT: int = paInt16
CHANNELS: int = 1
SAMPLING_RATE: int = 14410
FRAMES_PER_BUFFER: int = 256


class Client:
    """
    Client class
    """
    def __init__(self):
        self.audio = PyAudio()
        self.cfg = ConfigService('config/client_config.json')
        # Input and output audio stream initialisation
        self.stream_input = self.get_input_stream()
        self.stream_output = self.get_output_stream()

        IP = self.cfg.get_value('IP')
        print(IP)
        PORT = self.cfg.get_value('PORT')
        print(PORT)

        try:
            self._connect_to_server(IP, PORT)
        except Exception as e:
            logger.error(f"Failed to connect to server '{IP}:{PORT}': {e}")
        else:
            self._start_loop()

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

    def _connect_to_server(self, ip: str, port: int) -> None:
        """
        Connects to the Server on specified IP address and port.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Commented below is TCP stuff. No longer needed.
        # self.socket.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
        # self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 0)
        # self.socket.connect((ip, port))

        self.server_address = (ip, port)
        logger.info(f"Successfully connected to '{ip}:{port}'")

    def _start_loop(self) -> None:
        """
        Main loop in which the Client sends input stream data to the Server
        and handles output stream data from it.
        """
        while True:
            self._send_input_stream_to_server()
            data, _ = self.socket.recvfrom(FRAMES_PER_BUFFER*2)

            if data:
                self._handle_stream_from_server(data)

    def _send_input_stream_to_server(self) -> None:
        """
        Sends an audio input stream to the Server in bytes format
        """
        input_data = self._get_microphone_stream()
        self.socket.sendto(input_data, self.server_address)

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
