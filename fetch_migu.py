import requests
import re

def fetch_migu_url():
    # 这里写你原来的获取逻辑
    # 假设最后能拿到 url
    resp = requests.get("https://xxxx")  # 示例请求
    match = re.search(r"https://[^\s]+\.m3u8", resp.text)
    if match:
        return match.group(0)
    return None

if __name__ == "__main__":
    url = fetch_migu_url()
    if url:
        print(f"获取到的地址: {url}")

        # 写入 m3u 文件
        with open("migu.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            f.write("#EXTINF:-1,咪咕直播\n")
            f.write(url + "\n")

        print("已生成 migu.m3u 文件")
    else:
        print("未获取到地址")
