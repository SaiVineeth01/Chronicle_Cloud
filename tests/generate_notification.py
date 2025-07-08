from pydub.generators import Sine

tone = Sine(880).to_audio_segment(duration=300)  # 880Hz, 300ms
tone.export("notification.mp3", format="mp3")
