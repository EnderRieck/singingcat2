from datetime import datetime
from flask import render_template, request
from run import app
from wxcloudrun.dao import delete_counterbyid, query_counterbyid, insert_counter, update_counterbyid
from wxcloudrun.model import Counters
from wxcloudrun.response import make_succ_empty_response, make_succ_response, make_err_response

import os

from flask import Flask, request
import base64
import time

from audio_process import audio_process
import song_generate
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import librosa.display

from musicpy.daw import *
from musicpy import *
import recommend


@app.route('/')
def index():
    """
    :return: 返回index页面
    """
    return render_template('index.html')


@app.route('/api/count', methods=['POST'])
def count():
    """
    :return:计数结果/清除结果
    """

    # 获取请求体参数
    params = request.get_json()

    # 检查action参数
    if 'action' not in params:
        return make_err_response('缺少action参数')

    # 按照不同的action的值，进行不同的操作
    action = params['action']

    # 执行自增操作
    if action == 'inc':
        counter = query_counterbyid(1)
        if counter is None:
            counter = Counters()
            counter.id = 1
            counter.count = 1
            counter.created_at = datetime.now()
            counter.updated_at = datetime.now()
            insert_counter(counter)
        else:
            counter.id = 1
            counter.count += 1
            counter.updated_at = datetime.now()
            update_counterbyid(counter)
        return make_succ_response(counter.count)

    # 执行清0操作
    elif action == 'clear':
        delete_counterbyid(1)
        return make_succ_empty_response()

    # action参数错误
    else:
        return make_err_response('action参数错误')


@app.route('/api/count', methods=['GET'])
def get_count():
    """
    :return: 计数的值
    """
    counter = Counters.query.filter(Counters.id == 1).first()
    return make_succ_response(0) if counter is None else make_succ_response(counter.count)

<<<<<<< HEAD

=======
>>>>>>> 0ecb35562ca5bd6b9807f165c500613ba5435be4
# 传输音频的路由
@app.route('/audio', methods = ['POST', 'GET'])
def songRecommend():
    os.chdir(filepath)

    # 接收base64编码的音频
    audio_file = request.form.get('file')

    # 把base64编码变成2进制编码
    binary_audio = base64.b64decode(audio_file)
    #binary_audio = base64.decodebytes(audio_file)
    #audio_array = np.frombuffer(binary_audio, dtype=np.int16)  # 把2进制编码变成np数组

    # 写入原音频
    wav_result = open('./data/raw_audio/audio.wav', 'wb')
    wav_result.write(binary_audio)

    # 处理音频
    audio_process("./data/raw_audio/audio.wav")

    note = song_generate.pre_process(filepath)
    print("note: ", note)

    root = song_generate.get_fit_root(note)
    print(root)

    recom_list, pitch_list = recommend.recommend(root, note)
    print(recom_list, pitch_list)

    global pitch_dict
    pitch_dict = {key: value for key, value in zip(recom_list, pitch_list)}
    print(pitch_dict)

    return recom_list


@app.route('/song', methods=['POST'])
def song_gen():
    # 获取歌曲名称
    song_name = request.form.get('song_name')
    song_generate.song_generate(filepath, song_name, pitch_dict)

    with open('song.mp3', 'rb') as file:
        song = file.read()

    song = base64.b64encode(song)
    return song
<<<<<<< HEAD


=======
>>>>>>> 0ecb35562ca5bd6b9807f165c500613ba5435be4
