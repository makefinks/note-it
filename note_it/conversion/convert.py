import base64
import os
import fitz  # Import PyMuPDF
import asyncio
from anthropic import AsyncAnthropic



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


async def convert_images_to_text(image_folder, md_folder):

    # Create the folder if it doesnt exist
    if not os.path.exists(md_folder):
        os.makedirs(md_folder)

    # Semaphore to limit number of concurrent tasks
    semaphore = asyncio.Semaphore(2)

    async def bounded_convert_image_to_text(file_path):
        async with semaphore:
            return await convert_image_to_text(file_path, md_folder)

    tasks = []    

    # get all file paths and save them in a list
    for file in os.listdir(image_folder):
        if file.endswith('.png'):
            file_path = os.path.join(image_folder, file)
            task = bounded_convert_image_to_text(file_path)
            tasks.append(task)

    # run all the tasks
    await asyncio.gather(*tasks)



async def convert_image_to_text(image_path, md_folder):

    # get the page number from the image path
    page_number = image_path.split('_')[-1].split('.')[0]

    # Create an instance of the AsyncAnthropic class
    async_anthropic = AsyncAnthropic()

    # base 64 encode image
    image = open(image_path, 'rb')
    image = image.read()
    image_data = base64.b64encode(image).decode('utf-8')
    media_type = 'image/png'

    message = await async_anthropic.messages.create(
    model="claude-3-sonnet-20240229",
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
                        "text": "You are an expert in OCR (Optical Character Recognition) and are able to extract text from images with perfect accuracy. Extract the text from the image and provide me with a markdown-formatted output. Use headings and other markdown formatting where it makes sense. Directly output markdown-formatted text without a code block."
                    }
                ],
            }
        ],
    )

    # get the text from the message
    markdown = message.content[0].text

    # save each output file 
    with open(f'{md_folder}/page_{page_number}.md', 'w') as f:
        f.write(markdown)


async def main():
    
    convert_pdf_to_images('handwritten_short.pdf', "images")
    await convert_images_to_text("images", "output")

asyncio.run(main())
