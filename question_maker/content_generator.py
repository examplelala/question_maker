
from typing import List
import tiktoken
import os
from question_maker.logger import logger
def count_tokens(text, model="gpt-4"):
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))




def load_chapter_contents(file_paths:List[str]):
    content = {}
    section = {}
    chapter_titles = []
    for file_path in file_paths:
        if file_path.endswith(".txt") and os.path.isfile(file_path):  # 确保路径是文件
            chapter_key = os.path.basename(file_path).replace(".txt", "")  # 获取文件名并去掉扩展名
            with open(file_path, 'r', encoding='utf-8') as file:
                chapter_content = file.read().strip()  # 读取文件内容并去除前后空格
                content[chapter_key] = chapter_content  # 将内容存入字典
                section[chapter_key] = count_tokens(chapter_content)  # 统计章节token数
                chapter_titles.append(chapter_key)  # 存入章节名列表
        elif not file_path.endswith(".txt"):
            logger.error(f"{file_path} 不是txt文件,不被加载")
        elif not os.path.isfile(file_path):
            logger.error(f"{file_path} 不存在")
    if chapter_titles==[]:
        raise ValueError("没有找到有效的txt文件")

    logger.info(f"{chapter_titles} 加载成功")
    return content, section, chapter_titles








