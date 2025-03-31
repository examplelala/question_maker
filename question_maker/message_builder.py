import random

from langchain.text_splitter import RecursiveCharacterTextSplitter

class MessageBuilder:
    @staticmethod
    def generate_messages(content, difficulty, question_type):

        # 题型对应的 JSON 格式模板
        question_templates = {
            "选择题": {
                "instruction": f"根据以下内容生成{difficulty}难度的选择题，每道题应包含题目类别、题目内容、选项、正确答案和解析。",
                "format": {
                    "question_type": "选择题",
                    "question": "题目内容",
                    "options": ["选项A", "选项B", "选项C", "选项D"],
                    "answer": "正确答案",
                    "explanation": "解析"
                }
            },
            "填空题": {
                "instruction": f"根据以下内容生成{difficulty}难度的填空题，需填空的部分用 [] 括起来。",
                "format": {
                    "question_type": "填空题",
                    "question": "题目内容",
                    "answer": "正确答案",
                    "explanation": "解析"
                }
            },
            "判断题": {
                "instruction": f"根据以下内容生成{difficulty}难度的判断题，每道题应包含题目、正确答案和解析。",
                "format": {
                    "question_type": "判断题",
                    "question": "题目内容",
                    "answer": "正确答案",
                    "explanation": "解析"
                }
            },
            "简答题": {
                "instruction": f"根据以下内容生成{difficulty}难度的简答题，每道题应包含题目、正确答案和解析。",
                "format": {
                    "question_type": "简答题",
                    "question": "题目内容",
                    "answer": "正确答案",
                    "explanation": "解析"
                }
            }
        }
        example_questions = {
            "选择题": {
                "question_type": "选择题",
                "question": "2 + 2 等于多少？",
                "options": ["1", "2", "3", "4"],
                "answer": "4",
                "explanation": "2 加 2 等于 4。"
            },
            "填空题": {
                "question_type": "填空题",
                "question": "水的沸点是[]摄氏度。",
                "answer": "100",
                "explanation": "在标准大气压下，水的沸点是 100 摄氏度。"
            },
            "判断题": {
                "question_type": "判断题",
                "question": "2 + 2 = 4？",
                "answer": "正确",
                "explanation": "2 + 2 = 4。"
            },
            "简答题": {
                "question_type": "简答题",
                "question": "为什么天空是蓝色的？",
                "answer": "因为大气分子会散射太阳光，其中蓝光比红光散射得更强。",
                "explanation": "瑞利散射原理表明，短波长的光（如蓝光）比长波长的光（如红光）更容易被大气散射，因此我们看到的天空呈现蓝色。"
            }
        }
        # 获取当前题型的指令和格式
        question_data = question_templates.get(question_type, None)
        if not question_data:
            raise ValueError(f"未知的题型: {question_type}")

        instruction = question_data["instruction"]
        json_format = question_data["format"]

        # **使用 RecursiveCharacterTextSplitter 进行分块**
        splitter = RecursiveCharacterTextSplitter(chunk_size=7000,chunk_overlap=100)
        content_chunks = splitter.split_text(content)
        random.shuffle(content_chunks)
        system_prompt = (
            "你是一个专业且智能的 AI，擅长基于提供的内容精准生成高质量问题。请确保问题逻辑严谨、具有挑战性，并与内容高度相关。"
            "严格按照 JSON 格式输出，仅返回符合示例模板的 JSON 数据，不包含额外文本。确保所有字符串用英文的双引号包围，不要使用单引号。确保最后的JSON结果可以直接被JSON函数解析"
            f"{instruction}\n\n请严格按照以下JSON示例模板输出：[{json_format}]。一个题目的示例如下：[\n{example_questions[question_type]}\n]"
            f"多个题目的示例如下：[\n{example_questions[question_type]}\n\n{example_questions[question_type]}\n]"
        )
        # 构造 messages
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        # print(messages)
        for i, chunk in enumerate(content_chunks):
            if i<5:
                messages.append({"role": "user", "content": f"以下是内容第 {i+1} 部分，请根据所有提供的部分生成完整的问题：\n\n{chunk}"})

        return messages
if __name__ == '__main__':
    pass


