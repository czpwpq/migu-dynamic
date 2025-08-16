import requests
import re

url = "https://gitee.com/dream-deve/migu_video/raw/main/interface-aptv.txt"

resp = requests.get(url)
resp.encoding = "utf-8"
text = resp.text

# 提取 CCTV5+ 体育赛事
pattern = re.compile(r'#EXTINF:-1.*CCTV5\+体育赛事.*\n(http[^\s]+)')
match = pattern.search(text)

if match:
    m3u8_url = match.group(1)
    print("提取到的地址：", m3u8_url)
    with open("cctv5plus.m3u8", "w", encoding="utf-8") as f:
        f.write(m3u8_url + "\n")
else:
    print("未找到 CCTV5+ 体育赛事链接")
