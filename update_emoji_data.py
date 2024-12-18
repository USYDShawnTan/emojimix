import json
import re
import requests
import hashlib
import os

def download_metadata(url):
    """下载最新的 metadata.json 文件并返回内容"""
    response = requests.get(url)
    if response.status_code == 200:
        print("文件已成功下载")
        return response.text
    else:
        raise Exception(f"无法下载文件，状态码: {response.status_code}")

def calculate_content_hash(content):
    """计算内容的 SHA-256 哈希值"""
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()

def metadata_has_changed(content, hash_file_path):
    """检查 metadata.json 内容是否更新"""
    current_hash = calculate_content_hash(content)

    # 检查是否存在之前的哈希文件
    if os.path.exists(hash_file_path):
        with open(hash_file_path, 'r') as hash_file:
            previous_hash = hash_file.read().strip()
        # 比较哈希值
        if current_hash == previous_hash:
            print("metadata.json 文件没有变化")
            return False  # 没有变化

    # 若文件不存在或哈希值有变化，则更新哈希文件
    with open(hash_file_path, 'w') as hash_file:
        hash_file.write(current_hash)
    print("metadata.json 文件有变化")
    return True  # 文件有变化

def extract_gStaticUrl(content):
    """提取 gStaticUrl 链接并返回链接列表"""
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

    unique_emojis = [item["path"] for item in emoji_dict.values()]

    output_data = {
        "baseUrl": base_url,
        "emojis": unique_emojis
    }
    print("链接已去重并格式化")
    return output_data

def simplify_emoji_data(data):
    """进一步简化数据结构并按日期升序排序"""
    unique_dates = sorted(list({emoji.split('/')[0] for emoji in data["emojis"]}))  # 按升序排序
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

    # 对每个日期下的 emoji 列表进行排序
    for key in simplified_data["emojis"]:
        simplified_data["emojis"][key].sort()

    print("数据已简化并按日期升序排序，emoji 组也已排序")
    return simplified_data


# 自动更新流程
def main():
    # 文件路径和 URL
    metadata_url = "https://raw.githubusercontent.com/xsalazar/emoji-kitchen-backend/main/app/metadata.json"
    hash_file_path = "metadata_hash.txt"
    output_path = "emojimix_data.json"

    # 下载 metadata.json 内容
    content = download_metadata(metadata_url)

    # 检查 metadata.json 是否有更新
    if not metadata_has_changed(content, hash_file_path):
        print("文件内容未变动，跳过更新步骤")
        return  # 如果没有更新，退出程序

    # 如果文件有变化，继续执行以下处理
    urls = extract_gStaticUrl(content)
    formatted_data = reformat_urls(urls)
    simplified_data = simplify_emoji_data(formatted_data)

    # 保存最终简化后的数据
    with open(output_path, 'w', encoding='utf-8') as output_file:
        json.dump(simplified_data, output_file, ensure_ascii=False, indent=4)
    print(f"最终的简化数据已保存到 {output_path}")

# 运行自动更新脚本
if __name__ == "__main__":
    main()
