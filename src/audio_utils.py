import wave
import pyaudio
import numpy as np

class AudioRecorder:
    def __init__(self):
        """Initialize audio recording parameters"""
        self.chunk = 1024
        self.format = pyaudio.paFloat32
        self.channels = 1
        self.rate = 16000
        self.p = pyaudio.PyAudio()
        
    def record_audio(self, seconds):
        """Record audio for specified duration"""
        # Open audio stream
        stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        
        frames = []
        # Record audio in chunks
        for i in range(0, int(self.rate / self.chunk * seconds)):
            data = stream.read(self.chunk)
            frames.append(data)
            
        stream.stop_stream()
        stream.close()
        
        return frames
    
    def save_audio(self, frames, filename="input.wav"):
        """Save recorded audio to file"""
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        return filename