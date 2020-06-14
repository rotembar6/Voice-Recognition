# Voice-Recognition
This project is voice recognition by a user-selected code word.

# Requirements
pycharm with python 3.6.
You have to download this libraries: pyaudio, wave, numpy, flask.

# Installation
download the zip file and execute it. It should look like this:
* Server (Folder):
    * Recordings (Folder)
    * Templates (Folder)
    * Static (Folder)
    * Compare_Recordings.py
    * flask_handler.py
* Client (Folder) 
  * Recordings (Folder)
  * BaseRecorder.py
  * Recorder.py

# Usage
* Record "base recordings" with BaseRecorder.py (auto records 3 recordings) - saves in recordings
* Activate flask_handler.py and write http://localhost:5000/ in your browser.
* Upload the 3 recordings (don't change their names)
* From now, you can record with Recorder.py and upload it to the website. If its you - you will be transferred to other website.
