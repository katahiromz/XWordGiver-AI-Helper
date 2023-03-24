import tkinter as tk
import openai
import asyncio
import os

# このファイルのバージョン。
AI_HELPER_VERSION = "1.1"

#############################################################################
# APIヘルパーの設定。変更しても構いません。

# OpenAI (CharGPT) APIキー。環境変数「XW_OPENAI_API_KEY」から取得。
openai.api_key = os.environ["XW_OPENAI_API_KEY"]

# ChatAPIのモデル。
MODEL = "gpt-3.5-turbo"
#MODEL = "text-davinci-002"

# ヒント文章の文字数制限。
MAX_HINT_TEXT = 30

# 説明文の文字数制限。
MAX_DESC_TEXT = 60

# 時間切れまでの秒数。
MAX_TIME = 8

# ヒント候補の個数。
MAX_HINT_CANDIDATES = 3

# 説明文の候補の個数。
MAX_DESC_CANDIDATES = 2

# API問合せの待ち時間（秒）。
API_WAIT = 8

# タグをカンマ区切りで指定。
TAGS = "芸術,生活,道具,政治,災害,映画,算数,人体,感情,仕事,乗り物,車,自然,英語,家族,生物,国際,電気,学校,店,音楽,職業,建築,恋愛,歴史,海,病気,数学,医療,時間,地理,経営,旅行,論理,金融,趣味,言葉,社会,ファッション,子育て,鳥類,魚類,人間関係,暦,演劇,野球,天気,難解,動物,植物,会社,日本,機械,春,料理,技術,人生,農業,テレビ,夏,食べ物,科学,軍事,宗教,勝負,秋,スポーツ,交通,経済,文学,夜,冬,犯罪,不道徳,不幸,不快,成人向け,放送禁止"

#############################################################################

# グローバル変数。
global entry1
global text1
global text2
global text3

# 生成物をセット。
def do_set_text_1(str):
    text1.delete("1.0", "end")
    text1.insert("1.0", str)

# 生成物をセット。
def do_set_text_2(str):
    text2.delete("1.0", "end")
    text2.insert("1.0", str)

# 生成物をセット。
def do_set_text_3(str):
    text3.delete("1.0", "end")
    text3.insert("1.0", str)

# 行を処理する。
def do_line(line):
    import re
    # 箇条書きの先頭を取得し、削除する。
    match = re.match(r'^(\d+)\. ', line)
    number = ''
    if not(match is None):
        number = line[0:match.end()]
        line = line[match.end():]
    # かっこ・引用符を外す。
    line = re.sub(r'^「(.*)」$', '\\1', line)
    line = re.sub(r'^\"(.*)\"$', '\\1', line)
    # 最後の丸を除去する。
    line = re.sub(r'。$', '', line)
    # 丸かっこで囲まれた文字列を削除。
    line = re.sub(r'（.*?）', '', line)
    line = re.sub(r'\(.*?\)', '', line)
    # 文字数をはずす。
    line = re.sub(r'[\(（].*?文字[）\)]', '', line)
    line = re.sub(r' - \d+文字$', '', line)
    line = re.sub(r'の\d+文字$', '', line)
    # 最後の丸を除去する。
    line = re.sub(r'。$', '', line)
    # 箇条書きの先頭を元に戻す。
    line = number + line
    return line

# ヒント文章の生成。
def do_openai_1(text):
    try:
        do_try = True
        while do_try:
            query = "テキスト「{}」から{}字程度のクロスワードのヒント文章を{}つ考えて下さい。".format(text, MAX_HINT_TEXT, MAX_HINT_CANDIDATES)
            query += "放送禁止用語があれば「ERROR: 放送禁止用語です。」を追記して下さい。"
            do_set_text_1("問合せ中: " + query)
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": query},
                ],
                request_timeout = MAX_TIME,
            )
            do_set_text_1(query)
            # AIからの返信を取得する。
            str = response.choices[0]["message"]["content"].strip()
            if (text in str):
                continue
            # 再試行しない。
            do_try = False
            lines = str.split("\n")
            new_text = ""
            for line in lines:
                new_text += do_line(line).strip() + "\n"
            # 出力。
            do_set_text_1(new_text)
    except Exception as e:
        if type(e).__name__.strip() == "Timeout":
            do_set_text_1('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_1('ERROR: 例外発生: ', type(e).__name__)

# 説明文の生成。
def do_openai_2(text):
    try:
        import time
        time.sleep(API_WAIT)
        query = "テキスト「{}」から{}字程度の説明文を{}つ考えて下さい。".format(text, MAX_DESC_TEXT, MAX_DESC_CANDIDATES)
        do_set_text_2("問合せ中: " + query)
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": query},
            ],
            request_timeout = MAX_TIME,
        )
        # AIからの返信を取得する。
        str = response.choices[0]["message"]["content"].strip()
        # 出力。
        do_set_text_2(str)
    except Exception as e:
        if type(e).__name__.strip() == "Timeout":
            do_set_text_2('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_2('ERROR: 例外発生: ', type(e).__name__)

# カテゴリータグの生成。
def do_openai_3(text):
    try:
        import time
        time.sleep(API_WAIT * 2)
        tags = TAGS.split(',')
        tags_text = ""
        tags_num = 0
        for tag in tags:
            tags_text += "「[" + tag + "]」"
            tags_num += 1
        query = "カテゴリータグは{}の{}個です。テキスト「{}」に当てはまるカテゴリータグ（複数可、なるべく多く）をカンマ区切りで出力して下さい。".format(tags_text, tags_num, text)
        do_set_text_3("問合せ中: " + query)
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": query},
            ],
            request_timeout = MAX_TIME,
        )
        # AIからの返信を取得する。
        str = response.choices[0]["message"]["content"].strip()
        str = str.replace(', ', ',').replace(',', "\t")
        # 出力。
        do_set_text_3(str)
    except Exception as e:
        if type(e).__name__.strip() == "Timeout":
            do_set_text_3('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_3('ERROR: 例外発生: ', type(e).__name__)

# 実際の処理。
def do_work(text):
    import threading
    do_set_text_1("(生成中...)")
    thread1 = threading.Thread(target=do_openai_1, args=(text,))
    thread1.start()
    do_set_text_2("(生成中...)")
    thread2 = threading.Thread(target=do_openai_2, args=(text,))
    thread2.start()
    do_set_text_3("(生成中...)")
    thread3 = threading.Thread(target=do_openai_3, args=(text,))
    thread3.start()

# 生成アクション。
def onGenerate(e=None):
    text = entry1.get()
    do_work(text)

# コピーボタンのアクション。
def copyText():
    str = text1.get("1.0", "end")
    import pyperclip
    pyperclip.copy(str)

# リセットボタンのアクション。
def resetText():
    entry1.delete(0, tk.END)
    text1.delete("1.0", tk.END)
    text2.delete("1.0", tk.END)
    text3.delete("1.0", tk.END)

# GUIウィンドウの作成。
root = tk.Tk()
root.title("AIヘルパー Ver." + AI_HELPER_VERSION + " - クロスワード ギバー")
root.geometry("500x400")

# フレームの作成。
frame = tk.Frame(root)
frame.pack(side="top")

try:
    # ラベルの作成。
    label1 = tk.Label(frame, text="単語を入力して下さい:")
    label1.pack(side="left")

    # テキストボックスの作成
    entry1 = tk.Entry(frame, relief="sunken")
    entry1.pack(side="left")
    entry1.focus_set()
    entry1.bind('<Return>', onGenerate)

    # 「生成」ボタン。
    button1 = tk.Button(frame, text="生成", command=onGenerate)
    button1.pack(side="left")

    # リセットボタン。
    button2 = tk.Button(frame, text="リセット", command=resetText)
    button2.pack(side="left")

    # コピーボタン。
    button3 = tk.Button(frame, text="結果のコピー", command=copyText)
    button3.pack(side="left")
except:
    pass

# ラベルの作成。
label2 = tk.Label(root, text="ヒント文章:")
label2.pack(side="top")

# ヒント文章用の複数行テキストボックスの作成。
text1 = tk.Text(root, relief="sunken", bg="#cccccc", height=7)
text1.pack(side="top")

# ラベルの作成。
label3 = tk.Label(root, text="単語の説明:")
label3.pack(side="top")

# 説明用の複数行テキストボックスの作成。
text2 = tk.Text(root, relief="sunken", bg="#cccccc", height=7)
text2.pack(side="top")

# ラベルの作成。
label4 = tk.Label(root, text="カテゴリータグ（タブ区切り）:")
label4.pack(side="top")

# カテゴリータグ用の複数行テキストボックスの作成。
text3 = tk.Text(root, relief="sunken", bg="#cccccc")
text3.pack(side="top")

# GUIの起動。
root.mainloop()
