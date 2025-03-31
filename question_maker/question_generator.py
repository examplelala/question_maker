import json
import random
import time
from typing import List, Dict
from question_maker.logger import logger
import os

from question_maker.llm import LLM
from pathlib import Path


class QuestionGenerator:
    def __init__(self, chapter_titles: List[str], content: dict,
                 sections: dict, difficulty: str, question_type: str,
                 question_number: int):
        self.chapter_titles = chapter_titles
        self.content = content
        self.sections = sections
        self.difficulty = difficulty
        self.question_type = question_type
        self.question_number = question_number
        # self.model = LLM(api_key, base_url, model_name)
        self.model = LLM()

    def get_chapter_content_api(self, chapter_content_key):
        if isinstance(chapter_content_key, str):
            # 如果是字符串类型，直接取对应章节内容
            return self.content[chapter_content_key]
        elif isinstance(chapter_content_key, list):
            # 如果是列表类型，合并多个章节内容
            return "。".join([self.content[chapter] for chapter in chapter_content_key])
        else:
            raise ValueError("Invalid type for 'chapter_content'. It must be a string or a list.")

    @staticmethod
    def reselect_sections(chapter: List[str], sections: Dict[str, int], max_limit=128000):
        """
        重新选择小节，使得总 token 数不超过 max_limit，同时尽量均匀分配小节的选择机会。
        模型单次输入有长度限制，所以需要重新选择小节，使得总 token 数不超过 max_limit。
        :param chapter: 用户选择的章节列表（只考虑这些章节）
        :param sections: 一个字典，key 为章节名，value 为该章节的 token 数
        :param max_limit: 允许的最大 token 总数，默认 4000
        :return: 选中的小节列表，总 token 数
        """
        # 计算用户选择的章节的总 token 数
        total_tokens = sum(sections[sec] for sec in chapter if sec in sections)

        # 如果不超过 max_limit，直接返回
        if total_tokens <= max_limit:
            return chapter

        # 重新选择部分小节，使 token 数不超过 max_limit
        section_items = [(sec, sections[sec]) for sec in chapter if sec in sections]
        random.shuffle(section_items)  # 打乱顺序，确保不同小节都有机会被选中

        selected_chapter = []
        current_tokens = 0

        for sec, tokens in section_items:
            if current_tokens + tokens <= max_limit:
                selected_chapter.append(sec)
                current_tokens += tokens

        # print(f"总内容过多，随机选择部分小节：{selected_chapter}，总 token 数：{current_tokens}")
        return selected_chapter

    def generate_questions_api(self):
        # 获取章节内容
        chapter_content = self.get_chapter_content_api(self.chapter_titles)

        # 生成问题
        questions = self.model.generate_multiple_questions(
            chapter_content,
            self.difficulty,
            self.question_type,
            self.question_number)
        # print("大模型的输出")
        # print(questions)
        questions_dict = self.save_to_json_api(questions)
        return questions_dict

    def save_to_json_api(self, questions):
        BASE_DIR = Path(__file__).resolve().parent
        questions_dict = json.loads(questions)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        os.makedirs(f"{BASE_DIR}/questions", exist_ok=True)
        with open(f"{BASE_DIR}/questions/{self.difficulty}{self.question_type}{self.question_number}道{timestamp}.json", "w",
                  encoding="utf-8") as f:
            json.dump(questions_dict, f, ensure_ascii=False, indent=4)
        logger.info(f"题目缓存到{BASE_DIR}/questions文件夹下")
        return questions_dict


# 使用示例
if __name__ == "__main__":
    pass
