import re
import sys
import requests

SRC = "https://gitee.com/dream-deve/migu_video/raw/main/interface-aptv.txt"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0 Safari/537.36"
OUT = "cctv5plus.m3u"
CHANNEL = "CCTV5+体育赛事"

def fetch_source_text():
    r = requests.get(SRC, headers={"User-Agent": UA}, timeout=20)
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text

def extract_url(text, name=CHANNEL):
    # 匹配：#EXTINF...包含频道名 的下一行 http(s) 链接
    pattern = re.compile(r'#EXTINF:-1[^\n]*?' + re.escape(name) + r'[^\n]*?\n(https?://\S+)', re.M)
    m = pattern.search(text)
    return m.group(1).strip() if m else None

def write_m3u(url, path=OUT):
    new_content = f'#EXTM3U\n#EXTINF:-1 svg-name="{CHANNEL}" group-title="央视",{CHANNEL}\n{url}\n'
    try:
        with open(path, "r", encoding="utf-8") as f:
            old = f.read()
    except FileNotFoundError:
        old = None

    if old != new_content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("m3u内容有变化：已写入，将提交。")
        return True  # 有变化
    else:
        print("m3u内容无变化：不需要提交。")
        return False  # 无变化

def main():
    text = fetch_source_text()
    url = extract_url(text)
    if not url:
        print(f"未在源文件中找到频道：{CHANNEL}", file=sys.stderr)
        sys.exit(1)
    print("抓到链接：", url)
    changed = write_m3u(url)
    # 用于后续步骤判断是否需要提交
    if changed:
        sys.exit(0)
    else:
        # 退出码 78 表示“无需更改”，供 workflow 脚本判断
        sys.exit(78)

if __name__ == "__main__":
    main()
