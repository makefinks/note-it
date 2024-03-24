import asyncio
import os
from anthropic import AsyncAnthropic
import cv2
import streamlit as st
import xml.etree.ElementTree as ET
import re

def fix_headings_rulebased(markdown_text: str) -> str:
    
    lines = markdown_text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("#"):
            words = line.split(" ")

            # remove heading annotation if lenght of words is greater than 5
            if len(words) > 5:
                ## remove heading annotation (e.g. #, ##, ###, etc.)
                lines[i] = " ".join(words[1:])

    return "\n".join(lines)


async def fix_heading_for_file(file_path: str):
    
    # read contents of the file
    with open(file_path, "r") as f:
        markdown_text = f.read()

    prompt = ""
    with open("prompts/fix_headings.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    formated_prompt = prompt.format(markdown=markdown_text)
    
    # Create an instance of the AsyncAnthropic class
    async_anthropic = AsyncAnthropic()

    message = await async_anthropic.messages.create(
    model="claude-3-sonnet-20240229",
    max_tokens=4096,
    temperature=0.1,
    messages=[
            {
                "role": "user",
                "content": formated_prompt,
            }
        ],
    )

    # get the text from the message
    markdown = message.content[0].text

    """ # save the orginal markdown in temp file
    with open(f'{file_path}.org', 'w', encoding="utf-8") as f:
        f.write(markdown)
 """
    corrected_markdown = extract_tag_content(markdown, "corrected_markdown")

    # save each output file 
    with open(f'{file_path}', 'w', encoding="utf-8") as f:
        f.write(corrected_markdown)
    
async def fix_headings_llm(markdown_folder: str):
    sempahore = asyncio.Semaphore(2)

    async def bounded_fix_headings_for_file(file_path):
        async with sempahore:
            return await fix_heading_for_file(file_path)

    tasks = []
    for file in os.listdir(markdown_folder):
        file_path = os.path.join(markdown_folder, file)
        task = bounded_fix_headings_for_file(file_path)
        tasks.append(task)

    await asyncio.gather(*tasks)

def extract_tag_content(xml_text, tag_name):
    # Define a regex pattern to match the specified tag and capture its content
    pattern = f"<{tag_name}>(.*?)</{tag_name}>"

    # Search for the first occurrence of the pattern in the XML text
    match = re.search(pattern, xml_text, re.DOTALL)

    return match.group(1) if match else "No content found for the specified tag."



