# EmojiMix 🎨

一个高效的Emoji Kitchen数据处理工具，自动从Google的Emoji Kitchen服务获取最新的emoji组合数据，并提供多种格式的输出。

## ✨ 功能特性

- 🔄 **自动更新**: 智能检测元数据变化，避免重复处理
- 📊 **数据去重**: 自动保留最新版本的emoji组合，去除历史重复数据
- 🗜️ **双格式输出**: 支持原始JSON和紧凑JSON两种格式
- ⚡ **高效处理**: 优化的数据处理逻辑，快速处理大量数据
- 🔍 **完整性验证**: 自动验证数据完整性和一致性
- 📈 **压缩优化**: 紧凑格式可节省约44.5%的存储空间

## 📁 项目结构

```
emojimix/
├── src/                    # 源代码目录
│   └── update_emoji_data.py  # 主要的数据处理脚本
├── data/                   # 数据文件目录
│   ├── emojimix_data.json      # 原始格式数据（开发用）
│   ├── emojimix_data_compact.json  # 紧凑格式数据（生产用）
│   └── metadata_hash.txt       # 元数据哈希值（用于增量更新）
├── tests/                  # 测试文件目录
├── docs/                   # 文档目录
└── README.md              # 项目说明文档
```

## 🚀 快速开始

### 环境要求

- Python 3.6+
- requests 库

### 安装依赖

```bash
pip install requests
```

### 运行脚本

```bash
python src/update_emoji_data.py
```

## 📊 数据格式

### 原始JSON格式
```json
{
    "baseUrl": "https://www.gstatic.com/android/keyboard/emojikitchen/",
    "dates": ["20200101", "20200201", ...],
    "emojis": {
        "0": ["emoji1_emoji2", "emoji3_emoji4", ...],
        "1": ["emoji5_emoji6", ...],
        ...
    }
}
```

### 紧凑JSON格式
- 去除所有不必要的空格和换行
- 保持相同的数据结构
- 文件大小减少约44.5%

## 🔧 使用说明

### 数据更新流程

1. **下载元数据**: 从emoji-kitchen-backend获取最新的metadata.json
2. **哈希检查**: 比较当前哈希值与历史哈希值，判断是否需要更新
3. **URL提取**: 递归提取所有gStaticUrl链接
4. **数据处理**: 按日期分组，保留最新版本的emoji组合
5. **格式输出**: 生成原始格式和紧凑格式的JSON文件

### 文件说明

- `emojimix_data.json`: 格式化的JSON文件，便于开发和调试
- `emojimix_data_compact.json`: 紧凑格式，适合生产环境和网络传输
- `metadata_hash.txt`: 存储元数据的SHA-256哈希值，用于增量更新

### 数据压缩效果

| 格式 | 文件大小 | 压缩率 | 适用场景 |
|------|----------|--------|----------|
| 原始JSON | 4.3 MB | 0% | 开发和调试 |
| 紧凑JSON | 2.4 MB | 44.5% | 生产环境 |

## 🎯 核心算法

### 数据去重逻辑

```python
# 对于每个emoji组合，只保留最新日期的版本
if emoji_name not in emoji_dict:
    emoji_dict[emoji_name] = {"date": date, "path": emoji_path}
elif date > emoji_dict[emoji_name]["date"]:
    emoji_dict[emoji_name] = {"date": date, "path": emoji_path}
```

### URL模式解析

```
https://www.gstatic.com/android/keyboard/emojikitchen/{date}/{emoji_name}.png
```

- `date`: 8位数字日期格式 (YYYYMMDD)
- `emoji_name`: emoji组合名称 (emoji1_emoji2)

## 📈 性能特点

- **处理速度**: 可快速处理30万+个URL
- **内存效率**: 优化的数据结构，减少内存占用
- **存储优化**: 紧凑格式可节省44.5%存储空间
- **增量更新**: 智能检测变化，避免不必要的重复处理

## 🔍 数据来源

本项目的数据来源于 [emoji-kitchen](https://github.com/xsalazar/emoji-kitchen) 项目，通过处理Google的Emoji Kitchen服务的元数据生成。

## 📝 许可证

本项目遵循MIT许可证。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📞 联系方式

如有问题或建议，请通过GitHub Issues联系我们。
