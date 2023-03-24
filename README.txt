# クロスワード ギバー【AI ヘルパー】

## これは何？

プログラム言語PythonとChatGPTのAPIを使用して、クロスワードの作成を助けるツールです。

## 準備

まず最初に、Python 3.3以降をインストールして下さい。

次に、以下のコマンドを管理者権限のコマンドプロンプトで実行して下さい。

- pip install openai
- pip install asyncio
- pip install pyperclip
- pip install threading

これで準備は終わりです。

## 使い方

1. OpenAIのChatGPTの公式ページを開き、「Sign Up」「Log in」し、APIキーを取得して下さい。
2. システムの設定で環境変数「XW_OPENAI_API_KEY」を新たに作成し、ChatGPTのAPIキー（「sk-」から始まる）を指定して下さい。
1. ファイル「ai-helper.bat」をダブルクリックして下さい。
2. AIヘルパーが起動します。
3. 調べたい単語を入力してEnterキーを押して下さい。
4. ヒントなどが表示されます。

## 注意

- このプログラムは、OpenAIのサービスを利用しています。サービス内容の変更によっては利用できなくなる恐れがあります。
- この人工知能は、大規模言語モデルに基づいて動作しているため、不正確な情報や間違った情報を生成する恐れがあります。過度に信用するのは避けるべきです。
- Pythonのopenaiモジュールの仕様変更により、利用できなくなる恐れがあります。

## ライセンス

- MIT ライセンス

## 連絡先

- 片山博文MZ katayama.hirofumi.mz@gmail.com
