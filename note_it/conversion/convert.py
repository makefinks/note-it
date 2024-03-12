import base64
import os
import fitz  # Import PyMuPDF
import asyncio
from anthropic import AsyncAnthropic
import markdown2
import pdfkit
from PyPDF2 import PdfMerger
from note_it.conversion.postprocessing import fix_headings_rulebased

def create_pdf(md_folder, output_path):

    files = os.listdir(md_folder)
    markdown_files = [file for file in files if file.endswith('.md')]
    pdf_files = []

    # Convert each Markdown file to PDF
    for md_file in markdown_files:
        html = markdown2.markdown_path(f'{md_folder}/{md_file}')
        pdf_file = md_file.replace('.md', '.pdf')
        pdfkit.from_string(html, pdf_file)
        pdf_files.append(pdf_file)

    # Merge all PDF files
    merger = PdfMerger()
    for pdf in pdf_files:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

    # clean up individual PDF files
    for pdf in pdf_files:
        os.remove(pdf)

def merge_md_files(md_folder, output_path):
    
    files = os.listdir(md_folder)
    markdown_files = [file for file in files if file.endswith('.md')]

    # sort based on page number
    markdown_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))

    with open(output_path, 'w', encoding="utf-8") as outfile:
        for md_file in markdown_files:
            with open(f'{md_folder}/{md_file}', 'r', encoding="utf-8") as infile:
                outfile.write(f"\n{fix_headings_rulebased(infile.read())}")

    print("Markdown files merged successfully!")
    
    # delete individual markdown files
    for md_file in markdown_files:
        os.remove(f'{md_folder}/{md_file}')


def convert_pdf_to_images(pdf_document, save_folder):

    # Create the folder if it doesnt exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    
    pdf_document = fitz.open(pdf_document)  # Open the PDF file
    
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Set the desired DPI
        dpi = 100
        pix = page.get_pixmap(dpi=dpi)  # Render page to a pixmap with specified DPI
        
        output_file = f'{save_folder}/page_{page_num}.png'
        pix.save(output_file)
    
    pdf_document.close()
    print("PDF converted to images successfully!")


async def convert_images_to_text(image_folder, md_folder, model_name):

    # Create the folder if it doesnt exist
    if not os.path.exists(md_folder):
        os.makedirs(md_folder)

    # Semaphore to limit number of concurrent tasks
    semaphore = asyncio.Semaphore(2)

    async def bounded_convert_image_to_text(file_path):
        async with semaphore:
            return await convert_image_to_text(file_path, md_folder, model_name)

    tasks = []    

    # get all file paths and save them in a list
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            file_path = os.path.join(image_folder, file)
            task = bounded_convert_image_to_text(file_path)
            tasks.append(task)

    # run all the tasks
    await asyncio.gather(*tasks)
    print("Images converted to text successfully!")

    # delete images
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            os.remove(os.path.join(image_folder, file))


async def convert_image_to_text(image_path, md_folder, model_name):

    # get the page number from the image path
    page_number = image_path.split('_')[-1].split('.')[0]

    # Create an instance of the AsyncAnthropic class
    async_anthropic = AsyncAnthropic()

    # base 64 encode image
    image = open(image_path, 'rb')
    image = image.read()
    image_data = base64.b64encode(image).decode('utf-8')
    media_type = 'image/png'

    prompt = ""
    with open("prompts/extract_metaprompt.txt", "r") as f:
        prompt = f.read()

    message = await async_anthropic.messages.create(
    model=model_name,
    max_tokens=1024,
    messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )

    # get the text from the message
    markdown = message.content[0].text

    # save each output file 
    with open(f'{md_folder}/page_{page_number}.md', 'w', encoding="utf-8") as f:
        f.write(markdown)


async def convert(path_to_pdf: str, model_name: str) -> bool:
    print("Starting Conversion...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        convert_pdf_to_images(path_to_pdf, "images")
        await convert_images_to_text("images", "output", model_name)
        print("Text Conversion Done!")

        # create_pdf("output", "final_pdf.pdf")
        merge_md_files("output", "final.md")

        return True
    finally:
        loop.close()
