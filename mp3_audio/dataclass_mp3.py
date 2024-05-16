from dataclasses import dataclass


@dataclass
class Mp3Audio:
    all_headers: []
    all_sizes: []
    path: str = ''
    raw_data: bytes = b''
    audio_data: bytes = b''
    bit_rate: int = 0
    sample_rate: int = 0
    size: int = 0
    tag: bytes = b''
    count: int = 0
