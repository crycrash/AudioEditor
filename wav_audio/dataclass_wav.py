from dataclasses import dataclass


@dataclass
class WavAudioFile:
    """Класс данных для хранения данных об wav аудио дорожке"""
    chunk_size: int
    num_channels: int
    sample_rate: int
    bits_per_sample: int
    size_sec: int
    sub_chunk_2_size: int
