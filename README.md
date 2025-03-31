# 自动出题工具

本工具用于根据指定章节和难度，自动生成不同题型的题目。

## 功能说明

- 支持从txt文件中加载章节内容。
- 根据指定难度（简单、中等、困难）生成题目。
- 支持四种题型：简答题、判断题、选择题、填空题。
- 支持指定题目数量。
- 生成的题目将缓存至`question_maker/questions`目录下。

## 使用方法

### 参数配置

| 参数名         | 类型   | 说明                          |
| -------------- | ------ | ----------------------------- |
| chapter        | list   | 输入txt文件路径（列表形式）     |
| difficulty     | str    | 题目难度：简单、中等、困难     |
| question_type  | str    | 题型：简答题、判断题、选择题、填空题 |
| question_number| int    | 题目数量                       |

**注意：**
- 章节内容仅支持txt格式，输入其他格式会报错。
- pdf文件加载暂不支持。

## 示例代码

```python
# 参数示例
config = {
    "chapter": [
        "content路径1",
        r"content路径2"
    ],  # 输入txt文件路径，列表形式
    "difficulty": "困难",  # 选项：简单、中等、困难
    "question_type": "选择题",  # 题目类型：简答题、判断题、选择题、填空题
    "question_number": 3  # 题目个数
}

# 生成题目
questions = question_maker(**config)
```

## 缓存说明

- 生成的题目将自动缓存在`question_maker/questions`目录中，方便后续查看。

