# スクレイピングしてみた

## 概要

このプロジェクトは、指定したアーティストのアルバムデータをスクレイピングし、そのデータからアルバムタイトルや歌詞などを取得するツールです。さらに、取得した歌詞を要約し、簡潔な概要を提供します。データの取得元は [Uta-Net](https://www.uta-net.com/) です。Python の `BeautifulSoup` および `requests` ライブラリを使用してスクレイピングを実行し、取得したデータを要約する際には Python の `gensim` ライブラリを利用しています。

## 環境構築

1. リポジトリをクローン

    ```zsh
    git clone https://github.com/ShinodaHyuga/lyric_summary.git
    ```

2. Anaconda環境を作成

    ```zsh
    conda create --name lyric_summary python=3.8
    conda activate lyric_summary
    ```

3. ライブラリをインストール

    ```zsh
    conda install --file requirements.txt
    ```

## 使い方

1. スクレイプ対象を選択
   1. [Uta-Net](https://www.uta-net.com/)にアクセス
   2. **歌詞検索** から **アルバム検索** をクリック
   3. 任意のアーティストを選択
   4. URLをコピー
2. `scraping.py`の修正
   1. 先ほどコピーしたURLを`url`変数に定義（16行目）
   2. `scraping.pyの実行`
   3. `./result/{artist_name}_scraping.json`が作られる
3. `summarizing.py`の修正
   1. `artist_name`にアーティスト名（`./result/{artist_name}_scraping.json`の`{}の中身`）を定義（5行目）
   2. `summary.pyの実行`
   3. `./result/{artist_name}_summary.json

## バージョン履歴

- バージョン 1.0（2023/10/13）
  - 初期リリース
