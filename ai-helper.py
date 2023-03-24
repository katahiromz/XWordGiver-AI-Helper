# ai-helper.py - クロスワード ギバー AI ヘルパー
#
# Python+ChatGPTの能力により、クロスワード作成を強力に支援します。
# 起動には、付属のバッチファイル「ai-helper.bat」をお使い下さい。

# 必要なモジュールのインポート。
import tkinter as tk
import openai
import asyncio
import os
import time
import pyperclip
import sys

# このファイルのバージョン。
AI_HELPER_VERSION = "1.9"

#############################################################################
# APIヘルパーの設定。自由に変更しても構いません。

# CharGPTのAPIキー。環境変数「XW_OPENAI_API_KEY」から取得。
openai.api_key = os.environ["XW_OPENAI_API_KEY"]

# ChatGPTのモデル。
MODEL = "gpt-3.5-turbo"
#MODEL = "text-davinci-002"

# ヒント文章の文字数制限。
MAX_HINT_TEXT = 30

# 説明文の文字数制限。
MAX_DESC_TEXT = 60

# 時間切れまでの秒数。
MAX_TIME = 8

# API問合せの待ち時間（秒）。
API_WAIT = 8

# ヒント候補の個数。
MAX_HINT_CANDIDATES = 3

# 説明文の候補の個数。
MAX_DESC_CANDIDATES = 2

# タグをカンマ区切りで指定。
TAGS = "芸術,生活,道具,政治,災害,映画,算数,人体,感情,仕事,乗り物,車,自然,英語,家族,生物,国際,電気,学校,店,音楽,職業,建築,恋愛,歴史,海,病気,数学,医療,時間,地理,経営,旅行,論理,金融,趣味,言葉,社会,ファッション,子育て,鳥類,魚類,人間関係,暦,演劇,野球,天気,難解,動物,植物,会社,日本,機械,春,料理,技術,人生,農業,テレビ,夏,食べ物,科学,軍事,宗教,勝負,秋,スポーツ,交通,経済,文学,夜,冬,犯罪,不道徳,不幸,不快,成人向け,放送禁止"

#############################################################################

root = None
thread1 = thread2 = thread3 = None

# テキスト1をセット。
def do_set_text_1(str):
    global root, text1
    if root is None:
        return
    text1.delete("1.0", "end")
    text1.insert("1.0", str)

# テキスト2をセット。
def do_set_text_2(str):
    global root, text2
    if root is None:
        return
    text2.delete("1.0", "end")
    text2.insert("1.0", str)

# テキスト3をセット。
def do_set_text_3(str):
    global root, text3
    if root is None:
        return
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
    # 最後の丸を除去する。
    line = re.sub(r'。$', '', line)
    # 文字数をはずす。
    line = re.sub(r'[\(（\[【]\d+文字[）\)\]】]', '', line)
    line = re.sub(r' - \d+文字$', '', line)
    line = re.sub(r'の\d+文字$', '', line)
    # 最後の丸を除去する。
    line = re.sub(r'。$', '', line)
    # 箇条書きの先頭を元に戻す。
    line = number + line
    return line

# ヒント文章の生成。
def do_openai_1(text):
    global thread1
    try:
        do_try = True
        while do_try:
            # API問合せの前に待つ。
            time.sleep(API_WAIT * 0)
            # 問合せ文字列を表示する。
            query = "テキスト「{}」から{}字未満のクロスワードのヒント文章を{}つ考えて下さい。".format(text, MAX_HINT_TEXT, MAX_HINT_CANDIDATES)
            query += "放送禁止用語があれば「ERROR: 放送禁止用語です。」を追記して下さい。"
            do_set_text_1("問合せ中: " + query)
            # 実際に問合せを行う。
            response = openai.ChatCompletion.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": query},
                ],
                request_timeout = MAX_TIME,
            )
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
            # スレッドを無効化。
            thread1 = None
    except Exception as e:
        if thread1 is None:
            return
        if type(e).__name__.strip() == "Timeout":
            do_set_text_1('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_1('ERROR: 例外発生: ', type(e).__name__)

# 説明文の生成。
def do_openai_2(text):
    global thread2
    try:
        # API問合せの前に待つ。
        time.sleep(API_WAIT * 1)
        # 問合せ文字列を表示する。
        query = "テキスト「{}」から{}字未満の説明文を{}つ考えて下さい。".format(text, MAX_DESC_TEXT, MAX_DESC_CANDIDATES)
        do_set_text_2("問合せ中: " + query)
        # 実際に問合せを行う。
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
        # スレッドを無効化。
        thread2 = None
    except Exception as e:
        if thread2 is None:
            return
        if type(e).__name__.strip() == "Timeout":
            do_set_text_2('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_2('ERROR: 例外発生: ', type(e).__name__)

# カテゴリータグの生成。
def do_openai_3(text):
    global thread3
    try:
        # API問合せの前に待つ。
        time.sleep(API_WAIT * 2)
        # 各タグを[ ]で囲む。
        str = "[" + TAGS.replace(',', '],[') + "]"
        tags = str.split(',')
        tags_text = ""
        tags_num = 0
        for tag in tags:
            tags_text += "「" + tag + "」"
            tags_num += 1
        # 問合せ文字列を表示する。
        query = "カテゴリータグは{}の{}個です。テキスト「{}」に当てはまるカテゴリータグ（複数可、なるべく多く）をカンマ区切りで出力して下さい。".format(tags_text, tags_num, text)
        do_set_text_3("問合せ中: " + query)
        # 実際に問合せを行う。
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": query},
            ],
            request_timeout = MAX_TIME,
        )
        # AIからの返信を取得する。
        str = response.choices[0]["message"]["content"].strip()
        # タグの存在確認。
        str = str.replace(', ', ',').replace(',', "\t")
        generated_tags = str.split("\t")
        str = ""
        for tag in generated_tags:
            if tag in tags:
                str += tag
                str += "\t"
        # 出力。
        str = str.strip()
        do_set_text_3(str)
        # スレッドを無効化。
        thread3 = None
    except Exception as e:
        if thread3 is None:
            return
        if type(e).__name__.strip() == "Timeout":
            do_set_text_3('ERROR: API問合せの時間切れです（課金すれば？）。')
        else:
            do_set_text_3('ERROR: 例外発生: ', type(e).__name__)

# 実際の処理。
def do_work(text):
    global thread1, thread2, thread3
    import threading
    do_set_text_1("(生成中...)")
    thread1 = threading.Thread(target=do_openai_1, args=(text,))
    thread1.daemon = True
    thread1.start()
    do_set_text_2("(生成中...)")
    thread2 = threading.Thread(target=do_openai_2, args=(text,))
    thread2.daemon = True
    thread2.start()
    do_set_text_3("(生成中...)")
    thread3 = threading.Thread(target=do_openai_3, args=(text,))
    thread3.daemon = True
    thread3.start()

# 生成アクション。
def on_button1(e=None):
    global entry1
    text = entry1.get()
    do_work(text)

# リセットボタンのアクション。
def on_button2():
    global entry1, text1, text2, text3
    entry1.delete(0, tk.END)
    text1.delete("1.0", tk.END)
    text2.delete("1.0", tk.END)
    text3.delete("1.0", tk.END)

# コピーボタンのアクション。
def on_button3():
    global text1
    str = text1.get("1.0", "end")
    str = str.strip()
    pyperclip.copy(str)

# コピーボタンのアクション。
def on_button4():
    global text2
    str = text2.get("1.0", "end")
    str = str.strip()
    pyperclip.copy(str)

# コピーボタンのアクション。
def on_button5():
    global text3
    str = text3.get("1.0", "end")
    str = str.strip()
    pyperclip.copy(str)

# 終了時の処理を指定。
def on_quit():
    global root, thread1, thread2, thread3
    thread1 = thread2 = thread3 = None
    if not(root is None):
        root.quit()
        root.destroy()
        root = None
    sys.exit(0)

# GUIウィンドウの作成。
root = tk.Tk()
root.title("AIヘルパー Ver." + AI_HELPER_VERSION + " - クロスワード ギバー")
root.geometry("500x400")

# フレーム1の作成。
frame1 = tk.Frame(root)
frame1.pack(side="top")

# フレーム1の内部を作成。
if True:
    # ラベルの作成。
    label1 = tk.Label(frame1, text="単語を入力して下さい:")
    label1.pack(side="left")

    # テキストボックスの作成
    entry1 = tk.Entry(frame1, relief="sunken")
    entry1.pack(side="left")
    entry1.focus_set()
    entry1.bind('<Return>', on_button1)

    # 「生成」ボタン。
    button1 = tk.Button(frame1, text="生成", command=on_button1)
    button1.pack(side="left")

    # リセットボタン。
    button2 = tk.Button(frame1, text="リセット", command=on_button2)
    button2.pack(side="left")

# フレーム2の作成。
frame2 = tk.Frame(root)
frame2.pack(side="top")

# フレーム2の内部を作成。
if True:
    # ラベルの作成。
    label2 = tk.Label(frame2, text="ヒント文章:")
    label2.pack(side="left")

    # コピーボタン。
    button3 = tk.Button(frame2, text="コピー", command=on_button3)
    button3.pack(side="left")

# ヒント文章用の複数行テキストボックスの作成。
text1 = tk.Text(root, relief="sunken", bg="#cccccc", height=7)
text1.pack(side="top")

# フレーム3の作成。
frame3 = tk.Frame(root)
frame3.pack(side="top")

# フレーム3の内部を作成。
if True:
    # ラベルの作成。
    label3 = tk.Label(frame3, text="単語の説明:")
    label3.pack(side="left")

    # コピーボタン。
    button4 = tk.Button(frame3, text="コピー", command=on_button4)
    button4.pack(side="left")

# 説明用の複数行テキストボックスの作成。
text2 = tk.Text(root, relief="sunken", bg="#cccccc", height=7)
text2.pack(side="top")

# フレーム4の作成。
frame4 = tk.Frame(root)
frame4.pack(side="top")

# フレーム4の内部を作成。
if True:
    # ラベルの作成。
    label4 = tk.Label(frame4, text="カテゴリータグ（タブ区切り）:")
    label4.pack(side="left")

    # コピーボタン。
    button5 = tk.Button(frame4, text="コピー", command=on_button5)
    button5.pack(side="left")

# カテゴリータグ用の複数行テキストボックスの作成。
text3 = tk.Text(root, relief="sunken", bg="#cccccc")
text3.pack(side="top")

# 終了時の処理を指定。
root.protocol('WM_DELETE_WINDOW', on_quit)

# GUIの起動。
root.mainloop()
