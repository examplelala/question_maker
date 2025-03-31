import os
from typing import List
from question_maker.question_generator import QuestionGenerator
from question_maker.content_generator import load_chapter_contents
from question_maker.logger import logger


def question_maker(chapter: List[str], difficulty: str, question_type: str,
                   question_number: int) -> List[dict]:
    content, sections, chapter_titles = load_chapter_contents(chapter)
    qg = QuestionGenerator(content=content, sections=sections, chapter_titles=chapter_titles, difficulty=difficulty,
                           question_type=question_type, question_number=question_number)
    max_retries = 3
    for attempt in range(max_retries):
        try:
            logger.info(f"正在生成问题，第{attempt + 1}次尝试...")
            questions = qg.generate_questions_api()
            logger.info(f"成功生成{len(questions)}个{difficulty}{question_type}！\n题目内容：\n{questions}")
            return questions
        except Exception as e:
            logger.error(e)
            continue


if __name__ == '__main__':
    """       
        chapter，只能输入txt文件路径，其他会报错，pdf文件load我就不管了
        difficulty在：简单、中等、困难这三个中选择
        question_type：在简答题、判断题、选择题、填空题这几种题中选择
        question_number：题目个数
        question_maker/questions下有缓存的题目
    """

    # 演示示例
    config = {
        "chapter": ["content路径1",
                    r"content路径2"
                    ],  # 对应章节 输入txt文件路径，列表形式，逗号开
        "difficulty": "困难",  # 选项：简单、中等、困难
        "question_type": "选择题",  # 题目类型： 简答题、判断题、选择题、填空题
        "question_number": 3  # 题目个数
    }
    questions = question_maker(**config)  # 一个函数得到结果，结果是List[dict]形式
