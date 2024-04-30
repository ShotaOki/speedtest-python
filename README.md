# Python の並列実行検証

## 実行環境

Python 3.12 を利用します

## 実行準備

必要なライブラリをインストールします

```bash
pip install -r speed_test\requirements.txt
```

pytest をインストールします

```bash
pip install pytest
```

## 対象ファイルの準備

speedtest\\module_curl_s3.py を編集します、BUCKET_NAMES と FILES に自身のアカウントの S3 バケットとファイルを設定します

※FILES には、10 件以上のファイルを指定します

## 実行する

以下のコマンドを実行すると、ウォーターフォールチャートが作成されます

```bash
pytest tests\test_visualize.py
```

## 実行設定の変更

tests\\test_visualize.py の 171 行目以降を編集、\_test で始まっている関数の先頭のアンダーバーを消して、実行を有効化します。
