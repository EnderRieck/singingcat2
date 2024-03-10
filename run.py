# 创建应用实例
import sys

from wxcloudrun import app, recommend, song_generate

from flask import Flask, request

import os

from flask import Flask, request
import base64
import time

from wxcloudrun.audio_process import audio_process
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import librosa.display

from musicpy.daw import *
from musicpy import *

note = ""
pitch_dict = {}
filepath = os.getcwd()

# 启动Flask Web服务
if __name__ == '__main__':
    app.run(host=sys.argv[1], port=sys.argv[2])

