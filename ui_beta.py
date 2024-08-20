import tkinter as tk
from tkinter import messagebox, scrolledtext, Toplevel, Label
from prompts import load_prompt
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
    human_message = HumanMessage(content=description)

    messages = [system_message, human_message]

    response = llm(messages).content

    return response


def generate_markdown(formatted_description):
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
    prompt = load_prompt("mind_map_markdown_generator")

    system_message = SystemMessage(content=prompt)
    human_message = HumanMessage(content=formatted_description)

    messages = [system_message, human_message]

    response = llm(messages).content

    return response


def show_loading():
    loading_window = Toplevel(root)
    loading_window.title("Loading")
    loading_label = Label(loading_window, text="生成中，请稍候...")
    loading_label.pack(pady=20, padx=20)
    loading_window.geometry("200x100")
    loading_window.transient(root)
    loading_window.grab_set()
    root.update_idletasks()
    return loading_window


def on_generate_click():
    formatter_option = formatter_var.get()
    print(formatter_option)
    description = description_text.get("1.0", tk.END).strip()

    if not description:
        messagebox.showerror("Error", "请输入需要生成Markdown的内容")
        return

    formatter = None
    if formatter_option == "1":
        formatter = 'generative_formater'
    elif formatter_option == "2":
        formatter = 'criteria_formater'

    # 显示加载窗口
    loading_window = show_loading()

    root.after(100, lambda: process_generation(description, formatter, loading_window))


def parse_markdown(generated_markdown):
    lines = generated_markdown.splitlines()

    # 检查并删除第一行的 ```markdown
    if lines[0].strip() == "```markdown":
        lines = lines[1:]

    # 检查并删除最后一行的 ```
    if lines[-1].strip() == "```":
        lines = lines[:-1]

    # 将剩余的行重新组合成一个字符串
    return "\n".join(lines)


def process_generation(description, formatter, loading_window):
    if formatter:
        formatted_description = format_description(description, formatter)
    else:
        formatted_description = description

    generated_markdown = generate_markdown(formatted_description)
    generated_markdown = parse_markdown(generated_markdown)
    markdown_text.delete("1.0", tk.END)
    markdown_text.insert(tk.END, generated_markdown)

    U.dump_text(generated_markdown, "markdown/mind_map.md")

    # 关闭加载窗口
    loading_window.destroy()

    # 显示成功提示框
    messagebox.showinfo("Success", "Markdown生成并保存成功")


if __name__ == '__main__':
    # 创建Tkinter主窗口
    root = tk.Tk()
    root.title("Mind Map Markdown Generator")

    # Formatter选项
    formatter_label = tk.Label(root, text="请选择使用的formatter：")
    formatter_label.pack(pady=5)

    formatter_var = tk.StringVar(value="3")
    formatter_radiobutton1 = tk.Radiobutton(root, text="1. generative formater", variable=formatter_var, value="1")
    formatter_radiobutton1.pack(anchor="w")

    formatter_radiobutton2 = tk.Radiobutton(root, text="2. criteria formater (针对评分标准)", variable=formatter_var,
                                            value="2")
    formatter_radiobutton2.pack(anchor="w")

    formatter_radiobutton3 = tk.Radiobutton(root, text="3. 跳过", variable=formatter_var, value="3")
    formatter_radiobutton3.pack(anchor="w")

    # 描述输入框
    description_label = tk.Label(root, text="请输入需要生成Markdown的内容：")
    description_label.pack(pady=5)

    description_text = scrolledtext.ScrolledText(root, width=60, height=10)
    description_text.pack(pady=5)

    # 生成Markdown按钮
    generate_button = tk.Button(root, text="生成Markdown", command=on_generate_click)
    generate_button.pack(pady=10)

    # 显示Markdown结果
    markdown_label = tk.Label(root, text="生成的Markdown：")
    markdown_label.pack(pady=5)

    markdown_text = scrolledtext.ScrolledText(root, width=60, height=10)
    markdown_text.pack(pady=5)

    # 启动Tkinter事件循环
    root.mainloop()
