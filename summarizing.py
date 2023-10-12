import json
from gensim.summarization import summarize

# JSONファイルの読み込み
artist_name = ""  # ここにペースト
file_path = f"./result/{artist_name}_scraping.json"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except FileNotFoundError:
    print(f"Error: ファイル '{file_path}' が見つかりません。")
    exit(1)

# アルバム情報を格納するための辞書を初期化
album_data = {}

for album in data[artist_name]:
    titles = data[artist_name][album]["titles"]
    album_info = {}

    for i in range(len(titles)):
        title = titles[i]["title"]
        lyric = titles[i]["lyric"]

        # 要約を生成
        summary = summarize(text=lyric, ratio=0.1)

        # アルバム情報にタイトルと要約を追加
        album_info[title] = summary

    # アルバム情報を辞書に追加
    album_data[album] = album_info

# JSONファイルに書き込む
output_file_path = f"./result/{artist_name}_summary.json"
with open(output_file_path, "w", encoding="utf-8") as output_file:
    json.dump({"album": album_data}, output_file, ensure_ascii=False, indent=4)

print(f"アルバム情報をJSONファイルに書き込みました: {output_file_path}")
