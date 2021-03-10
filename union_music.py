import wave


def join_waves(n, count):
    '''
    inputs : list of filenames
    output : output filename
    '''
    inputs = [str(n) + '.wav' for n in range(1, count)] #切り取りしたフォルダ内場所
    output = 'C:/Users/kotap/OneDrive/Desktop/systemB/COMPRESITION/output.wav'#統合ファイル
    try:
        fps = [wave.open(f, 'r') for f in inputs]
        fpw = wave.open(output, 'w')

        fpw.setnchannels(fps[0].getnchannels())
        fpw.setsampwidth(fps[0].getsampwidth())
        fpw.setframerate(fps[0].getframerate())

        for fp in fps:
            fpw.writeframes(fp.readframes(fp.getnframes()))
            fp.close()
        fpw.close()

    except wave.Error as e:
        print(e)

    except Exception as e:
        print('unexpected error ->' + str(e))
