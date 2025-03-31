import os

from openai import OpenAI
from question_maker.message_builder import MessageBuilder

os.environ["DEEPSEEK_API_KEY"] = "xxxxxx"
#os.environ["OPENAI_API_KEY"] = "xxxxxx"

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_url = "https://api.openai.com/v1/"
openai_model = "gpt-4o-mini"

deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
deepseek_url = "https://api.deepseek.com/"
deepseek_model = "deepseek-chat"



class LLM:
    '''
    用的openai框架，注意更换api_key,base_url,model这三个参数对应就行
    '''

    def __init__(self, api_key=deepseek_api_key, base_url=deepseek_url, model=deepseek_model):
        # 初始化API连接
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def generate_multiple_questions(self, chapter_content, difficulty="简单", question_type="选择题",
                                    question_number=1):
        """
        根据章节内容和难度生成问题
        :param chapter_content: 章节内容
        :param difficulty: 题目难度，简单、中等、困难
        :param question_type: 题目类型，选择题、填空题、判断题、简答题
        :return: 生成的题目和答案
        """
        # 生成prompt
        messages = MessageBuilder.generate_messages(chapter_content, difficulty, question_type)
        prompt = f"\n请一次性生成{question_number}道{question_type}，并确保这些题目之间没有显著的相似性。不同的题目之间用两个回车隔开。"
        messages += [{"role": "user", "content": prompt}]
        # 调用DeepSeek的API生成题目
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        # 保存生成的题目

        return response.choices[0].message.content


if __name__ == '__main__':
    pass
