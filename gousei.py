import numpy as np
import librosa
import librosa.display
import re
import glob
import os
import sys
import cv2
from scipy.spatial.distance import euclidean
from matplotlib import pyplot as plt
from pathlib import Path
from itertools import chain
from matching_kashi import kashi_data
from cut_wav import cut_music
from union_music import join_waves
from decide_time import decide

exts = ["mp3", "m4a"]

# ユーザーの持っている曲(サビにしたい)のパス
os.chdir('./YOUR_MUSIC')
dirpath = os.getcwd()
p_mp3 = Path(dirpath)

# ユーザーの曲をwav変換して格納するパス
os.chdir('./WAV_CREATE')
dirpath = os.getcwd()
p_wav = str(Path(dirpath))

# サビ抽出した複数のwavを入れるパス 最後に/は入れとく
os.chdir('./WAV_CUT/')
dirpath = os.getcwd()
p_cut = str(Path(dirpath))


filepaths = list(chain.from_iterable(
    [list(p_mp3.glob(f"*.{ext}")) for ext in exts]))

count = 1


for path_music in filepaths:  # YOUR_MUSICフォルダから情報取得
    asename_without_ext = os.path.splitext(os.path.basename(path_music))[0]
    print(count, ":", asename_without_ext)

    pcm_data, sampling_rate = librosa.load(
        p_wav + '/' + asename_without_ext + '.wav')
    # wav変換は各自でやってください
    # フォルダはWAV_CREATE内に

    # 移動平均でdbを小さくする
    v = np.array([0.25, 0.25, 0.25, 0.25])
    a = np.convolve(pcm_data, v)

    # パワースペクトラムの値を求める
    num_bins = 256
    frame_shift = int(0.01*sampling_rate)
    frame_size = int(0.02*sampling_rate)

    # 移動平均を考慮しないパワースペクトラム
    power_spectrum = np.abs(librosa.stft(
        pcm_data, n_fft=num_bins*2, win_length=frame_size, hop_length=frame_shift))**2
    log_spectrum_1 = librosa.power_to_db(power_spectrum)

    # 移動平均を考慮するパワースペクトラム
    power_spectrum = np.abs(librosa.stft(
        a[::4], n_fft=num_bins*2, win_length=frame_size, hop_length=frame_shift))**2
    log_spectrum = librosa.power_to_db(power_spectrum)

    # パワースペクトラムによる音の最大値の座標(時間)の取得
    sam = []
    san = 0
    for x in log_spectrum_1.T:
        for y in x:
            san = san+y
        sam.append(san)
        san = 0

    max_value = max(sam)
    max_index = sam.index(max_value)

    # パワースペクトラムの類似度
    power_spectrum_Similar = np.corrcoef(np.transpose(log_spectrum))
    print("音源類似度完成")

    data_kashi = kashi_data(path_music)  # matching_kashi.pyから歌詞の類似度を取得

    if data_kashi != "No":

        # 歌詞の行列をパワースぺクトラムの行列の大きさと揃える
        takasa, yoko = power_spectrum_Similar.shape[:2]
        size = (takasa, yoko)
        re_data_kashi = cv2.resize(data_kashi, size)

        # plt.imshow(re_data_kashi)
        # plt.title(asename_without_ext)
        # plt.colorbar()
        # plt.show()

        # ２つの類似度を足し合わせる
        conb = power_spectrum_Similar + re_data_kashi
    else:  # 足し合わせられない時
        conb = power_spectrum_Similar

    # plt.imshow(conb)
    # plt.title(asename_without_ext)
    # plt.colorbar()
    # plt.show()

    time = decide(conb, max_index, sam)  # サビ時間決定
    print(time)

    # サビ時間を使ってほしい部分の切り抜き
    cut_music(p_wav + '/' + asename_without_ext + '.wav', time, count)

    count = count + 1
# 切り抜きしたwavファイルを統合する
join_waves(p_cut, count)
