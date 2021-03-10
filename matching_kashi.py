from alkana_code.alkana.main import get_kana
from romaji import change_word
# from edit_distance import edit_distance
from Leven import distance
from get_kashi import get_kashi_data
import re
import numpy as np
import matplotlib.pyplot as plt


def check_word(read_data):
    # ひらがな、かたかな、漢字
    re_japanese = re.compile(r'^([あ-ん]|[\u30A1-\u30F4]|[\u4E00-\u9FD0]|ー|-)+$')
    # 英文only
    re_english = re.compile(r'^([a-z]|[A-Z]|\s|　|\')+$')
    # 日本語と英語 実装していない
    # re_mix = re.comple(r'^([あ-ん]|[\u30A1-\u30F4]|[\u4E00-\u9FD0]|[a-z]|[A-Z])+$')

    check_data = []

    # 1フレーズごとの使用言語の確認
    for i in range(len(read_data)):
        if re_japanese.fullmatch(read_data[i]):  # 全て日本語の場合
            check_data.append(change_word(read_data[i]))
        elif re_english.fullmatch(read_data[i]):  # 全て英語の場合
            Eng_sen = read_data[i].split()
            # print(Eng_sen)
            for j in range(len(Eng_sen)):
                Eng_sen[j] = Eng_sen[j].lower()  # 全て小文字に
                Eng_sen[j] = get_kana(Eng_sen[j])  # カタカナ変換
            # print(Eng_sen)
            StrA = "".join(str(Eng_sen))
            check_data.append(change_word(StrA))  # 文字列に直してローマ字変換
    # print(len(check_data))
    return check_data


# def main():
def kashi_data(path_music):
    data = get_kashi_data(path_music)  # web検索で歌詞の読み込み
    if data == 'No':  # 読み込みできなかった場合
        print("URLの取得失敗")
        return data

    #print("get_kashi_data fin")
    # print(data)
    data2 = check_word(data)  # 1フレームごとの歌詞を全てローマ字に変換
    # print(data2)
    # print("check_word")
    data3 = distance(data2)  # レーベンシュタイン計算を行う
    #print("distance fin")

    coef = np.corrcoef(data3)
    print("歌詞類似度生成終了")

    return coef
