import json
import os
import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# 歌ネットのURL
base_url = "https://www.uta-net.com"

# データを格納する辞書
data_dict = {}

# アルバム一覧ページ
url = ""  # ここにペースト

try:
    response = requests.get(url)
    response.raise_for_status()  # エラーハンドリング
except requests.exceptions.RequestException as e:
    print(f"Error in HTTP request: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")
albums = soup.find_all("table", class_="album_table")

# アーティスト名を取得
artist_name = soup.find("th", class_="artist_name")
artist_name = artist_name.text
print(f"artist is {artist_name}")

# 待機時間を定数として定義
WAIT_TIME = 1

for album in albums:
    album_title = album.select_one("div.album_title a").text  # アルバム名
    album_release_date = album.select("div.album_title dd")[0].text  # アルバム発売日

    links = album.select("li a")

    for link in links:
        a = base_url + (link.get("href"))

        try:
            # 歌詞詳細ページ
            response = requests.get(a)
            response.raise_for_status()  # エラーハンドリング
        except requests.exceptions.RequestException as e:
            print(f"Error in HTTP request for details page: {e}")
            continue  # エラーが発生した場合は次のリンクへ

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h2").text  # タイトル

        # 発売日などを取得
        detail = soup.find("p", class_="detail").text

        # 発売日を抽出
        match = re.search(r"\d{4}/\d{2}/\d{2}", detail)
        if match:
            title_release_date = datetime.strptime(match.group(), "%Y/%m/%d").date()
        else:
            title_release_date = None

        # 歌詞を取得
        lyric = "\n".join(soup.find("div", {"id": "kashi_area"}).stripped_strings)

        # 辞書にデータを格納
        if artist_name not in data_dict:
            data_dict[artist_name] = {}
        if album_title not in data_dict[artist_name]:
            data_dict[artist_name][album_title] = {
                "album_release_date": album_release_date,
                "titles": []
            }

        data_dict[artist_name][album_title]["titles"].append({
            "title": title,
            "title_release_date": str(title_release_date) if title_release_date else None,
            "lyric": lyric
        })

        # サーバーに負荷を与えないため待機
        time.sleep(WAIT_TIME)

# カレントディレクトリを取得
current_directory = os.getcwd()
# "result"ディレクトリのパスを作成
result_directory = os.path.join(current_directory, "result")
# "result"ディレクトリが存在しない場合、作成する
if not os.path.exists(result_directory):
    os.mkdir(result_directory)

# データをJSONファイルに書き込む
output_file = f"./result/{artist_name}_scraping.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=4)

print(f"スクレイピング結果をJSONファイルに書き込みました: {output_file}")
