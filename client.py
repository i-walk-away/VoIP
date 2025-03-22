"""
The Client object connects to the Server and exchanges data with it
"""
import socket

from pyaudio import PyAudio, paInt16, Stream

from src.utils.logger import logger
from src.services.config_service import ConfigService


class Client:
    """
    Client class
    """
    FORMAT: int = paInt16
    CHANNELS: int = 1
    SAMPLING_RATE: int = 14410
    FRAMES_PER_BUFFER: int = 256

    def __init__(self):
        self.config = ConfigService('config/client_config.json')

        # Audio interface, input and output stream initialization
        self.audio = PyAudio()
        self.stream_input: Stream = self.get_input_stream()
        self.stream_output: Stream = self.get_output_stream()

        # Connection
        self.ip: str = self.config.get('IP')
        self.port: int = self.config.get('PORT')
        self.server_address: tuple[str, int] = (self.ip, self.port)

        try:
            self._connect_to_server()
        except Exception as e:
            logger.error(f"Failed to connect to server '{self.ip}:{self.port}': {e}")
        else:
            self._start_loop()

    def get_input_stream(self) -> Stream:
        """
        Returns the input Stream
        """
        return self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.SAMPLING_RATE,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
        )

    def get_output_stream(self) -> Stream:
        """
        Returns the output Stream
        """
        return self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.SAMPLING_RATE,
            output=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
        )

    def _connect_to_server(self) -> None:
        """
        Connects to the Server on specified IP address and port.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        logger.info(f"Successfully connected to '{self.ip}:{self.port}'")

    def _start_loop(self) -> None:
        """
        Main loop in which the Client sends input stream data to the Server
        and handles output stream data from it.
        """
        while True:
            self._send_input_stream_to_server()
            data, _ = self.socket.recvfrom(512)

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
        return self.stream_input.read(self.FRAMES_PER_BUFFER, exception_on_overflow=False)

    def _handle_stream_from_server(self, stream: bytes) -> None:
        """
        Handles the output stream data from the Server
        :param stream: Output audio stream to handle
        """
        self.stream_output.write(stream)


client = Client()
