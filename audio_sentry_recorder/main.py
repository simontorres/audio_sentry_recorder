import os
import audioop
import pyaudio
import wave

from datetime import datetime
from pathlib import PurePath

from utils import get_args, get_filename

class AudioSentryRecorder(object):

    def __init__(self) -> None:
        self.args = None
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 44100  # Record at 44100 samples per second
        self.seconds = 2
        self.signal_power_threshold = 100

        self.p = pyaudio.PyAudio()  # Create an interface to PortAudio

        self.start = None

    def __call__(self, args=None):

        if args is None:
            self.args = get_args()
        else:
            self.args = args

        self.signal_power_threshold = self.args.threshold
        
        stream = self.p.open(format=self.sample_format,
                             channels=self.channels,
                             rate=self.fs,
                             frames_per_buffer=self.chunk,
                             input=True)
        frames = []  # Initialize array to store frames
        recording = []
        self.start = None
        try:
            while True:
                
                # Store data in chunks for 3 seconds
                for i in range(0, int(self.fs / self.chunk * self.seconds)):
                    data = stream.read(self.chunk)
                    frames.append(data)
                
                rms = audioop.rms(b''.join(frames), 2)
                print(f"Listening... Sound level: {rms}, threshold: {self.signal_power_threshold}", end="\r")

                if rms > self.signal_power_threshold:
                    if not self.start:
                        self.start = datetime.now()
                    recording.extend(frames)
                    frames = []
                else:
                    if not self.start:
                        continue
                    print('Finished recording', end="\r")

                    self.end = datetime.now()
                    filename, folder_name = get_filename(start=self.start, end=self.end, save_to_folder=self.args.save_to_folder)
                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    print(f"Recording saved to: {filename}")

                    self.save_to_file(filename=filename, recording=recording)
                    self.start = None
                    recording = []
                    frames = []
        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            self.p.terminate()

    def save_to_file(self, filename: PurePath, recording):

        # Save the recorded data as a WAV file
        with wave.open(os.fspath(filename), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.sample_format))
            wf.setframerate(self.fs)
            wf.writeframes(b''.join(recording))


if __name__ == '__main__':
    sentry = AudioSentryRecorder()
    sentry()