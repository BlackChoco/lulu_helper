import openai
import os
from volcenginesdkarkruntime import Ark

def extract_high_frequency_words_and_expressions(text_file_path,system_prompt):
    # client = openai.OpenAI(
    # base_url="https://yunwu.ai/v1",
    # api_key="sk-7cV8G6WhtWYW91zp86W5OaiZfnK5lQXnj3LGbM2OOSurIqu9"
    # )
    # 豆包调用
    client = Ark(
        api_key="2733a4ee-2c11-415d-b8a2-91c616cfaf52"#"2733a4ee-2c11-415d-b8a2-91c616cfaf52"
        )

    with open(text_file_path, 'r', encoding='utf-8') as file:
        conversation = file.read()

        # 设计一个 conversation 模板
        conversation_template = """
        Here is conversation you need to summarize:
        {conversation}
        """
        # 使用模板生成 conversation
        conversation = conversation_template.format(conversation=conversation)

    try:
        # 使用新的 API 接口
        response = client.chat.completions.create(
            model="ep-20250213162235-gpw8r",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation}
            ],
            temperature=1,
            max_tokens=4096,  # Add max_tokens parameter
            top_p=0.7,  # Add top_p parameter
            frequency_penalty=0  # Add frequency_penalty parameter
        )
        # 提取生成的文本
        summary = response.choices[0].message.content

        knowledge_name = os.path.splitext(os.path.basename(text_file_path))[0]
        dir_name = os.path.dirname(text_file_path)
        output_path = os.path.join(dir_name,knowledge_name+'_summary.txt')

        with open(output_path, 'a', encoding='utf-8') as file:
            file.write(summary)

        return summary
    except Exception as e:
        print(f"请求出错: {e}")
        return None
