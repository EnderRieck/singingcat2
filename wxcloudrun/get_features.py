from pydub import AudioSegment
from scipy.fft import fft
import numpy as np
from scipy.io import wavfile
import musicpy.daw as mpd

def fft_(filepath):
    # 将音频变成数组
    sound = AudioSegment.from_file(filepath)
    samples = sound.get_array_of_samples()

    # 将音频标准化
    max_amplitude = np.max(np.abs(samples))
    samples = samples / max_amplitude

    # 获取变换结果的长度和采样率
    N = samples.shape[0]
    T = 1 / sound.frame_rate

    # 计算傅里叶变换
    yf = 2.0 / N * np.abs(fft(samples))[:N // 2]


    # 创建频率轴
    xf = np.linspace(0.0, 1.0 / (2.0 * T), N // 2)

    # 找到最大振幅对应的索引
    max_index = np.argmax(yf[:N // 2])

    # 获取对应的主频率值
    main_frequency = xf[max_index]/2

    print(main_frequency)

    return main_frequency

def get_times(audioname, instname):
    def get_volume(filename):
        audio = AudioSegment.from_file(filename)

        audio = audio.split_to_mono()[0]
        audio = np.array(audio.get_array_of_samples())
        volume = np.mean(np.abs(audio))

        return volume
    v1 = get_volume(audioname)
    v2 = get_volume(instname)

    times = v2*5/v1
    return times


def sin_wave(_freq):
    duration = 3           # 持续时间（秒）
    sampling_rate = 44100  # 采样率（每秒采样点数）
    frequency = int(_freq)        # 频率（Hz）

    # 生成时间轴
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    # 生成正弦波信号
    sin_wave = np.sin(2 * np.pi * frequency * t)

    # 将信号转换为 16 位整数格式
    sin_wave_int = np.int16(sin_wave * 32767)

    # 将信号写入 WAV 文件
    wavfile.write(r'.\data\raw_audio\sine_wave.wav', sampling_rate, sin_wave_int)


#sin_wave(440)