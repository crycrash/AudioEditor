from dataclasses import dataclass


@dataclass
class Mp3AudioFrame:
    """Класс данных для хранения данных об MP3 фрейме"""
    header: []
    marker: int
    padded: bool
    bit_rate_bits: int
    sample_rate: int = 0
    size: int = 0
