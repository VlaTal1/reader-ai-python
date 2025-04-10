import json
import math
import re

import PyPDF2


def remove_extra_newlines(text):
    return re.sub(r'\n+', '\n', text)

def read_pdf(file_path: str):
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            return text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def split_text_into_parts(text: str, num_parts: int):
    paragraphs = re.split('\n', text.strip())

    paragraphs_per_part = math.ceil(len(paragraphs) / (num_parts))

    parts = []
    current_part = ""

    for i, paragraph in enumerate(paragraphs):
        current_part += paragraph + "\n"
        if (i + 1) % paragraphs_per_part == 0 or (i + 1) == len(paragraphs):
            parts.append(current_part.strip())
            current_part = ""

    return parts

def get_json_from_response(text):
    json_match = re.search(r"<json_format>(.*?)</json_format>", text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1).strip()
    else:
        markdown_match = re.search(r"```json(.*?)```", text, re.DOTALL)
        if markdown_match:
            json_str = markdown_match.group(1).strip()
        else:
            raise ValueError("JSON не найден ни в формате <json_format>, ни в формате Markdown.")

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка декодирования JSON: {e}")