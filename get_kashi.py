import requests
import bs4
from bs4 import BeautifulSoup
from read_music import read
import re


def get_url(path_music):
    # キーワードを使って検索する
    data = read(path_music)  # 0タイトル，1アルバム，2アーティストの順
    list_keywd = [data[2], data[0], 'J-Lyric.net']
    key1 = str(list_keywd[0])
    key1 = key1[2:-2]  # 配列の['']の部分を削除
    key2 = str(list_keywd[1])
    key2 = key2[2:-2]
    key3 = str(list_keywd[2])

    # リクエストヘッダー　
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

    # 上位20件まで検索結果を取得
    url = 'https://www.google.co.jp/search?hl=ja&num=20&q=' + str(list_keywd)
    # print(url)

    # 接続
    response = requests.get(url, headers=headers)

    # HTTPステータスコードをチェック（200以外は例外処理）
    response.raise_for_status()

    # 取得したHTMLをパース
    soup = bs4.BeautifulSoup(response.content, 'html.parser')

    # 検索結果のタイトルとリンクを取得
    ret_link = soup.select('.yuRUbf > a')  # クラスチェック大事

    title_list = []
    url_list = []

    for i in range(len(ret_link)):
        #	タイトルのテキスト部分を取得
        title_txt = ret_link[i].get_text()

    #	リンクのみを取得し、余計な部分を削除する
        url_link = ret_link[i].get('href').replace('/url?q=', '')

        title_list.append(title_txt)
        url_list.append(url_link)

    # 欲しいやつ取得
    for i in range(len(title_list)):
        word = str(title_list[i])
        if key1 in word and key2 in word and key3 in word:
            return str(url_list[i])
            break
    No_url = 'No'
    return str(No_url)


def get_kashi_data(path_music):
    # Webページを取得して解析する
    load_url = get_url(path_music)
    # urlが取得できたか確認する
    if load_url == 'No':
        return load_url

    html = requests.get(load_url)
    soup = BeautifulSoup(html.content, "html.parser")

    kashi = soup.find(id="Lyric")  # webのLyricクラスを切り取り

    for i in kashi.select("br"):
        i.replace_with('\n')

    kashi.text.strip()  # \nに変更後，分割に使用
    kashi_list = kashi.text.splitlines()

    code_regex = re.compile(
        '[!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]')  # 記号削除に使用

    for i in range(len(kashi_list)):
        kashi_list[i] = kashi_list[i].replace('　', '')  # 空白文字をなくす
        kashi_list[i] = code_regex.sub('', kashi_list[i])  # 記号文字を削除

    kashi_list = [x for x in kashi_list if x]  # 空リスト削除
    # print(kashi_list)
    return kashi_list
