from prompts import load_prompt, load_descriptions
import utils as U

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import os

from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def format_description(description):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = load_prompt("generative_formater")
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
    description = input("请输入需要生成Markdown的内容： ")

    formatted_description = format_description(description)
    markdown = generate_markdown(formatted_description)

    U.dump_text(markdown, "markdown/mind_map.md")


if __name__ == '__main__':
    main()
