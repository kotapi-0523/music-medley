def cut_music(path, time, count):
    from pydub import AudioSegment
    import os

    # wavファイルのパス　例（D:\music\melody.wav）
    file_path = path
    out_path1 = "./WAV_CUT/"

    # 元ファイル名にcountをつけてリネーム
    out_path = os.path.join(str(count) + '.wav')

    # wavファイルの読み込み
    sound = AudioSegment.from_wav(file_path)

    # 0～10秒を抽出
    sound1 = sound[time * 10 - 15000:time * 10 + 20000]

    # リネームされて出力
    sound1.export(out_path1 + out_path, format="wav")
