import json
import re
import requests

def download_metadata(url):
    """下载最新的 metadata.json 文件并返回内容"""
    response = requests.get(url)
    if response.status_code == 200:
        print("文件已成功下载")
        return response.text
    else:
        raise Exception(f"无法下载文件，状态码: {response.status_code}")

def extract_gStaticUrl(content):
    """提取 gStaticUrl 链接并返回链接列表"""
    # 使用正则表达式查找所有 gStaticUrl 的链接
    urls = re.findall(r'"gStaticUrl":"(https://www\.gstatic\.com/[^"]+)"', content)
    print(f"共提取到 {len(urls)} 个链接")
    return urls

def reformat_urls(urls):
    """去重并筛选最新的日期"""
    base_url = "https://www.gstatic.com/android/keyboard/emojikitchen/"
    emojis = [url.replace(base_url, "") for url in urls]

    emoji_dict = {}
    for emoji_path in emojis:
        match = re.match(r"^(\d{8})/(.+)$", emoji_path)
        if match:
            date, path = match.groups()
            if path in emoji_dict:
                if date > emoji_dict[path]["date"]:
                    emoji_dict[path] = {"date": date, "path": emoji_path}
            else:
                emoji_dict[path] = {"date": date, "path": emoji_path}

    # 只保留最新的路径部分
    unique_emojis = [item["path"] for item in emoji_dict.values()]

    output_data = {
        "baseUrl": base_url,
        "emojis": unique_emojis
    }
    print("链接已去重并格式化")
    return output_data

def simplify_emoji_data(data):
    """进一步简化数据结构"""
    unique_dates = list({emoji.split('/')[0] for emoji in data["emojis"]})
    date_index_map = {date: index for index, date in enumerate(unique_dates)}

    simplified_data = {
        "baseUrl": data["baseUrl"],
        "dates": unique_dates,
        "emojis": {}
    }

    for emoji_path in data["emojis"]:
        parts = emoji_path.split('/')
        date = parts[0]
        emoji_name = parts[-1]
        
        date_index = date_index_map[date]
        if str(date_index) not in simplified_data["emojis"]:
            simplified_data["emojis"][str(date_index)] = []
        simplified_data["emojis"][str(date_index)].append(emoji_name)

    print("数据已简化")
    return simplified_data

# 自动更新流程
def main():
    # 文件路径和 URL
    metadata_url = "https://raw.githubusercontent.com/xsalazar/emoji-kitchen-backend/main/app/metadata.json"
    output_path = "emojimix_data.json"

    # 下载 metadata.json 内容
    content = download_metadata(metadata_url)

    # 提取 gStaticUrl 链接
    urls = extract_gStaticUrl(content)

    # 去重并筛选最新日期
    formatted_data = reformat_urls(urls)

    # 简化数据结构并保存为 emojimix_data.json
    simplified_data = simplify_emoji_data(formatted_data)
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(simplified_data, output_file, ensure_ascii=False, indent=4)

    print(f"最终的简化数据已保存到 {output_path}")

# 运行自动更新脚本
if __name__ == "__main__":
    main()
