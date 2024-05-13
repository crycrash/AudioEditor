from pydub import AudioSegment
from audioWav import AudiofileWav
sound = AudioSegment.from_mp3('/Users/milana/Downloads/sample4.mp3')
sound.export("/Users/milana/Downloads/sam123x.wav", format="wav")

a = AudiofileWav("/Users/milana/Downloads/sam123x.wav")
a.take_header_config()
a.speed_multiplying(2.0)
