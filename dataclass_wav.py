from dataclasses import dataclass


@dataclass
class WavAudioFile:
    chunk_size: 0
    format: 0
    sub_chunk_1_size: 0
    num_channels: 0
    sample_rate: 0
    byte_rate: 0
    block_align: 0
    bits_per_sample: 0
    audio_format: 0
    file_name: ''
    sub_chunk_2_id: 0
    size_sec: 0
    sub_chunk_2_size: 0
