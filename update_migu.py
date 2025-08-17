import re
import requests

def fetch_migu_url():
    # ⚠️ 这里用你的实际可用入口 URL（例如咪咕赛事页面的地址）
    entry_url = "https://example.migu.cn/live/xxxx"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    resp = requests.get(entry_url, headers=headers, timeout=10)
    resp.raise_for_status()

    # ⚠️ 用正则匹配 m3u8 地址（你之前日志里抓到过的）
    match = re.search(r"https://[^\"']+\.m3u8", resp.text)
    if match:
        return match.group(0)
    else:
        return None


def save_m3u(url):
    with open("migu.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("#EXTINF:-1,咪咕直播\n")
        f.write(url + "\n")
    print("已生成 migu.m3u 文件")


if __name__ == "__main__":
    url = fetch_migu_url()
    if url:
        print("获取到的地址:", url)
        save_m3u(url)
    else:
        print("未获取到地址")
