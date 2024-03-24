import asyncio
import os
from anthropic import AsyncAnthropic
import cv2
import streamlit as st

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
    model=st.session_state.model,
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

    # save each output file 
    with open(f'{file_path}', 'w', encoding="utf-8") as f:
        f.write(markdown)
    

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

