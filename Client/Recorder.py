import pyaudio
import wave
import os

"""
Using pyaudio library in oreder to record the user say his password
and save it as a wav file.
CHUNK - how many samples are in a frame that stream will be read.
Format - Captures the audio in hexadecimal format.
Channels - Stereo
Rate - Sample rate is the number of samples of audio carried per second, measured in Hz => 44100 Hz (standart)

"""

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2


def record(p):
    """
    Records audio from a connected audio input device (microphone/webcam...).
    :param p: pyaudio library object.
    :return: a list of audio frames that were recorded
    """
    frames = []
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, frames_per_buffer=CHUNK)

    print("recording")
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("done")

    stream.stop_stream()
    stream.close()
    p.terminate()
    return frames


def write_wav_file(frames, p, save_path):
    """
    Receives the audio frames list and writes a wav file.
   The file is closed when the writing is finished.
    :param frames: list of audio frames.
            p: a pyaudio library object.
    :return: None
    """

    wf = wave.open(save_path, 'w')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


def last_record():
    save_path = input('Write a path to save the recording: ')
    if not os.path.exists(save_path):
        os.mkdir(save_path.split('/')[-1])
    p = pyaudio.PyAudio()
    audio_frames_list = record(p)
    write_wav_file(audio_frames_list, p, str(save_path + '\\4.wav'))


def main():
    last_record()

if __name__ == '__main__':
    main()