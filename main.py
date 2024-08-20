from prompts import load_prompt, load_descriptions
import utils as U

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import os

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def format_description(description, formatter):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = load_prompt(formatter)
    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(description)

    messages = [system_message, human_message]

    response = llm(messages).content

    print(response)

    return response


def generate_markdown(formatted_description):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = load_prompt("mind_map_markdown_generator")

    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(formatted_description)

    messages = [system_message, human_message]

    response = llm(messages).content

    return response


def main():
    print("请选择使用的formatter（输入1/2/3）\n1.generative formater\n2.criteria formatter (针对评分标准)\n3.跳过")
    formatter = input(">")
    if int(formatter) == 1:
        formatter = 'generative_formater'
    elif int(formatter) == 2:
        formatter = 'criteria_formater'
    else:
        formatter = None

    print("请输入需要生成Markdown的内容")
    description = input(">")

    if not formatter:
        markdown = generate_markdown(description)
        U.dump_text(markdown, "markdown/mind_map.md")
        return

    formatted_description = format_description(description, formatter)
    markdown = generate_markdown(formatted_description)

    U.dump_text(markdown, "markdown/mind_map.md")


if __name__ == '__main__':
    main()
