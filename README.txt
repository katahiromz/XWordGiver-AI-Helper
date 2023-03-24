# クロスワード ギバー【AI ヘルパー】

## これは何？

プログラム言語Pythonと人工知能ChatGPTのAPIを使用して、クロスワードの作成を助けるツールです。

## 準備

1. まず最初に、Python 3.3以降をインストールし、環境変数PATHを通して下さい。
2. 次に、以下のコマンドを管理者権限のコマンドプロンプトで実行して下さい。
    - python -m pip install --upgrade pip
    - python -m pip install openai
    - python -m pip install asyncio
    - python -m pip install pyperclip
    - python -m pip install pykakasi
3. OpenAIのChatGPTの公式ページをブラウザで開き、「Sign Up」「Log in」し、APIキーを取得して下さい。
4. システムの詳細設定で環境変数「XW_OPENAI_API_KEY」を新たに作成し、ChatGPTのAPIキー（「sk-」から始まる）を指定して下さい。

これで準備は終わりです。

## 使い方

1. ファイル「ai-helper.bat」をダブルクリックして下さい。
2. AIヘルパーが起動します。
3. 調べたい単語を入力してEnterキーを押して下さい。
4. ヒントなどが表示されます。

## 注意

- このプログラムは、OpenAIのサービスを利用しています。サービス内容の変更によっては利用できなくなる恐れがあります。
- この人工知能は、大規模言語モデルに基づいて動作しているため、不正確な情報や間違った情報を生成する恐れがあります。過度に信用するのは避けるべきです。
- Pythonのopenaiモジュールの仕様変更により、利用できなくなる恐れがあります。
- APIキーが情報漏洩すると、不正利用される恐れがあります。

## ライセンス

- MIT ライセンス

## 連絡先

- 片山博文MZ katayama.hirofumi.mz@gmail.com
