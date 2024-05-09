from dataclasses import dataclass

@dataclass
class Mp3Audio:
    path: str
    raw_data: bytes
    audio_data: bytes
    bit_rate: int
    sample_rate: int
    size: int
    tag: bytes
    count: int
    all_headers: []
    all_sizes: []
