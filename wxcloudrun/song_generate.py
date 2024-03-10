import time

import musicpy.structures as mps
import musicpy.daw as mpd
import musicpy.musicpy as mpm
import librosa
import soundfile
from dataclasses import dataclass
import os
import get_features
import numpy as np


# 预处理
def pre_process(filepath):
    """
    对原音频进行预处理

    首先找到音频的主频，并根据音名对应的音高，计算与之最近的音

    之后将原音频调整到与该音频相同

    最后从这个音生成一整套音源

    :param filepath: 当前目录的绝对路径
    :return: note: str 调整好的猫叫音高
    """
    # 进行快速傅里叶变换，找主频
    freq0 = round(float(get_features.fft_(filepath + r".\data\raw_audio\audio1.wav")), 1)


    # 对循环中的变量进行初始化
    note = ""
    k = 0.0
    last_freq = 0.0
    last_note = ""

    # 找到最贴近的音
    for i, (note_, freq) in enumerate(note_dict.items()):
        print("for last note: ", last_note, "for note_: ", note_)
        freq = float(freq)
        if i == 35:
            raise "Note is too high!"
        if freq0 < freq:
            if i == 0:
                raise "Note is too low!"
            k_h = 12 * np.log2(freq/freq0)
            k_l = 12 * np.log2(last_freq/freq0)
            if abs(k_h) > abs(k_l):
                print("lastnote: ", last_note)
                note = last_note
                k = k_l
                break
            else:
                print("note: ", note_)
                note = note_
                k = k_h
                break
        last_freq, last_note = freq, note_
    print("note: ", note)

    # 读取原音频
    pitch1 = mpd.pitch(filepath + "/data/raw_audio/audio1.wav", format="wav")
    # 原音频标准化
    pitch1.pitch_shift(k)
    pitch1.set_note(note)

    # 生成电子乐器
    pitch1.export_sound_files("./data",
                             folder_name="cat_sound",
                             start="A0",
                             end="C8",
                             format="wav",
                             mode="librosa")
    time.sleep(3)
    return note



def get_fit_root(note: str):
    """
    找到合适的调的根音，也就是猫叫音的下行五度音

    :param note: 预处理里面调整好的猫叫的音高
    :return: str
    """
    # 拆分出音名和音高数
    if note[1] == "#":
        note_name = note[0] + "#"
        note_pitch = int(note[2])
    else:
        note_name = note[0]
        note_pitch = int(note[1])

    # 算出这个音的下行五度音
    key = note_transform_dict[note_name]
    # 定好这几个音的音高数
    if note_name in ["C", "C#", "D", "D#", "E"]:
        note_pitch -= 1

    if key == "B":
        note_pitch += 1

    # 将音归并到选定的五个调里
    if key in note_standard_dict.keys():
        key = note_standard_dict[key]

    root = key + f"{note_pitch}"

    return root


# 歌曲数据类
@dataclass
class Song_data:
    """
    存储一首歌的数据的类
    :param song_str: 首调的乐谱str
    :param volume: 猫叫音量
    :param inst_volume: 伴奏音量
    :param inst_path: 伴奏文件路径
    """
    key: str
    song_str: str
    volume: int
    inst_volume: int
    inst_path: str
    bpm: int

def key_to_chord(song_str: str, note: str):
    """
    将乐谱中的首调表示替换成固定调表示
    :param song_str: 歌曲谱的str
    :param note: 调整好的猫叫音高
    :return: str
    """
    scale = get_scale(note)
    s = song_str
    # 替换同一个八度内的音
    for i in range(7):
        s = s.replace(f"<{i+1}>", scale[i])

    # 替换高一个八度内的音
    scale_high = [n[: -1] + str(int(n[-1]) + 1) for n in scale]
    for i in range(7):
        s = s.replace(f"<{i+1}+>", scale_high[i])

    # 替换低一个八度内的音
    scale_low = [n[: -1] + str(int(n[-1]) - 1) for n in scale]
    for i in range(7):
        s = s.replace(f"<{i+1}->", scale_low[i])

    return s


# 生成歌曲
def song_generate(filepath, name: str, pitch_dict):
    """
    生成歌曲
    :param filepath: 当前目录的绝对路径
    :param data: 选择的歌曲
    :param root: 挑选的歌的根音
    :return: None
    """
    # 将歌曲名字符串转换为歌曲对象
    data = song_dict[name]

    # 准备乐谱
    print("pitch_dict: ", pitch_dict)
    key = data.key + str(pitch_dict[data.key])
    song_str = key_to_chord(data.song_str, key)
    print(song_str)
    song_chord = mps.chord(song_str)

    # 创建工程
    song = mpd.daw(2, name="song")
    # 加载音源
    print(os.getcwd())
    song.load(0, filepath + r"\data\cat_sound")

    # 调整音量
    song_chord.set_volume(50 * get_features.get_times(filepath + r"\data\raw_audio\audio1.wav", filepath + data.inst_path))
    print(song_chord.get_volume()[0])

    # 伴奏
    inst_sound = mpd.sound(filepath + data.inst_path)
    inst_chord = mpd.audio_chord([inst_sound.sounds], interval=0, duration=200, volume=data.inst_volume)

    # 生成歌曲
    piece = mps.piece(tracks=[song_chord, inst_chord],
                      daw_channels=[0, 1],
                      bpm=data.bpm)

    #song.play(piece, wait=True)
    # 导出歌曲
    os.chdir(filepath)
    song.export(piece, filename="song.mp3")




# ———————————————————歌曲数据———————————————————



# 小星星
# 配置歌谱
verse1_str1 = '<1>[.4; .4], <1>[.4; .4], <5>[.4; .4], <5>[.4; .4], <6>[.4; .4], <6>[.4; .4], <5>[.4; .2], <4>[.4; .4], <4>[.4; .4], <3>[.4; .4], <3>[.4; .4], <2>[.4; .4], <2>[.4; .4], <1>[.4; .2], '
verse2_str1 = '<5>[.4; .4], <5>[.4; .4], <4>[.4; .4], <4>[.4; .4], <3>[.4; .4], <3>[.4; .4], <2>[.4; .2], '
song_str1 = verse1_str1 + verse2_str1 * 2 + verse1_str1[0: -2]
# 创建数据对象
little_star = Song_data(key="C",
                        song_str=song_str1,
                        volume=13500,
                        inst_volume=100,
                        inst_path=r"data/instrument/little_star_inst.m4a",
                        bpm=70)

# 生日快乐歌
# 配置歌谱
song_str2 = 'r[.2; .], <5->[3/16; .], <5->[.16; .], <6->[.4; .], <5->[.4; .], <1>[.4; .], <7->[.2; .], <5->[3/16; .], <5->[.16; .], <6->[.4; .], <5->[.4; .], <2>[.4; .], <1>[.2; .], <5->[3/16; .], <5->[.16; .], <5>[.4; .], <3>[.4; .], <1>[.4; .], <1>[.4; .], <7->[.4; .], <4>[3/16; .], <4>[.16; .], <3>[.4; .], <1>[.4; .], <2>[.4; .], <1>[.4; .]'
happy_birthday = Song_data(key="E",
                           song_str=song_str2,
                           volume=0,
                           inst_volume=100,
                           inst_path=r"data/instrument/happy_birthday_inst.m4a",
                           bpm=95)

# 歌曲列表
song_dict = {"little_star": little_star,
             "happy_birthday": happy_birthday}

# ———————————————————长列表和函数———————————————————

def get_scale(note:str):
    """
    输入一个音，输出这个音的上行音阶
    :param note: 输入的音
    :return: StrList
    """
    # 拆分出音名和音高数
    if note[1] == "#":
        note_name = note[0] + "#"
        note_pitch = int(note[2])
    else:
        note_name = note[0]
        note_pitch = int(note[1])

    key_dict = {"A": [f"A{note_pitch}", f"B{note_pitch}", f"C#{note_pitch + 1}", f"D{note_pitch + 1}", f"E{note_pitch + 1}", f"F#{note_pitch + 1}", f"G#{note_pitch + 1}"],
                "A#": [f"A#{note_pitch}", f"C{note_pitch + 1}", f"D{note_pitch + 1}", f"D#{note_pitch + 1}", f"F{note_pitch + 1}", f"G{note_pitch + 1}", f"A{note_pitch + 1}"],
                "B": [f"B{note_pitch}", f"C#{note_pitch + 1}", f"D#{note_pitch + 1}", f"E{note_pitch + 1}", f"F#{note_pitch + 1}", f"G#{note_pitch + 1}", f"A#{note_pitch + 1}"],
                "C": [f"C{note_pitch}", f"D{note_pitch}", f"E{note_pitch}", f"F{note_pitch}", f"G{note_pitch}", f"A{note_pitch}", f"B{note_pitch}"],
                "C#": [f"C#{note_pitch}", f"D#{note_pitch}", f"F{note_pitch}", f"F#{note_pitch}", f"G#{note_pitch}", f"A#{note_pitch}", f"C{note_pitch + 1}"],
                "D": [f"D{note_pitch}", f"E{note_pitch}", f"F#{note_pitch}", f"G{note_pitch}", f"A{note_pitch}", f"B{note_pitch}", f"C#{note_pitch + 1}"],
                "D#": [f"D#{note_pitch}", f"F{note_pitch}", f"G{note_pitch}", f"G#{note_pitch}", f"A#{note_pitch}", f"C{note_pitch + 1}", f"D{note_pitch + 1}"],
                "E": [f"E{note_pitch}", f"F#{note_pitch}", f"G#{note_pitch}", f"A{note_pitch}", f"B{note_pitch}", f"C#{note_pitch + 1}", f"D#{note_pitch + 1}"],
                "F": [f"F{note_pitch}", f"G{note_pitch}", f"A{note_pitch}", f"A#{note_pitch}", f"C{note_pitch + 1}", f"D{note_pitch + 1}", f"E{note_pitch + 1}"],
                "F#": [f"F#{note_pitch}", f"G#{note_pitch}", f"A#{note_pitch}", f"B{note_pitch}", f"C#{note_pitch + 1}", f"D#{note_pitch + 1}", f"F{note_pitch + 1}"],
                "G": [f"G{note_pitch}", f"A{note_pitch}", f"B{note_pitch}", f"C{note_pitch + 1}", f"D{note_pitch + 1}", f"E{note_pitch + 1}", f"F#{note_pitch + 1}"],
                "G#": [f"G#{note_pitch}", f"A#{note_pitch}", f"C{note_pitch + 1}", f"C#{note_pitch + 1}", f"D#{note_pitch + 1}", f"F{note_pitch + 1}", f"G{note_pitch + 1}"]}

    return key_dict[note_name]

note_dict = {"C4": 261.6,
             "C#4": 277.2,
             "D4": 293.7,
             "D#4": 311.1,
             "E4": 329.6,
             "F4": 349.2,
             "F#4": 370.0,
             "G4": 392.0,
             "G#4": 415.3,
             "A4": 440.0,
             "A#4": 466.2,
             "B4": 493.9,

             "C5": 523.3,
             "C#5": 554.4,
             "D5": 587.3,
             "D#5": 622.3,
             "E5": 659.3,
             "F5": 698.5,
             "F#5": 740.0,
             "G5": 784.0,
             "G#5": 830.6,
             "A5": 880.0,
             "A#5": 932.3,
             "B5": 987.8,

             "C6": 1046.5,
             "C#6": 1108.7,
             "D6": 1174.7,
             "D#6": 1244.5,
             "E6": 1318.5,
             "F6": 1396.9,
             "F#6": 1480.0,
             "G6": 1568.0,
             "G#6": 1661.2,
             "A6": 1760.0,
             "A#6": 1864.7,
             "B6": 1975.5}

note_transform_dict = {"A": "E",
                       "A#": "F",
                       "B": "F#",
                       "C": "G",
                       "C#": "G#",
                       "D": "A",
                       "D#": "A#",
                       "E": "B",
                       "F": "C",
                       "F#": "C#",
                       "G": "D",
                       "G#": "D#"}

note_standard_dict = {"B": "C",
                      "C#": "D",
                      "D#": "E",
                      "F": "E",
                      "F#": "G",
                      "G#": "A",
                      "A#": "A"}