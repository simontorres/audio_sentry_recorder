import os
import audioop
import pyaudio
import wave

from datetime import datetime

def get_filename(start: datetime, end: datetime, format: str = 'wav') -> str:
    folder_name = start.strftime("%Y%m%d")
    name_start = start.strftime("%Y%m%d_%H%M%S")
    name_end = ""

    filename = f"{folder_name}/{name_start}{name_end}.{format}"
    return filename, folder_name

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 44100  # Record at 44100 samples per second
seconds = 2
signal_power_threshold = 100

p = pyaudio.PyAudio()  # Create an interface to PortAudio


stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)
frames = []  # Initialize array to store frames
recording = []
start = None
try:
    while True:
        
        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        
        rms = audioop.rms(b''.join(frames), 2)
        print(f"Listening... Sound level: {rms}", end="\r")

        if rms > signal_power_threshold:
            if not start:
                start = datetime.now()
            recording.extend(frames)
            frames = []
        else:
            if not start:
                continue
            print('Finished recording', end="\r")

            end = datetime.now()
            filename, folder_name = get_filename(start=start, end=end)
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            print(f"Recording saved to: {filename}")

            # Save the recorded data as a WAV file
            wf = wave.open(filename, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(recording))
            wf.close()
            start = None
            recording = []
            frames = []
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()
