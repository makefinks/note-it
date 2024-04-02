# note-it

I wrote this application to test OCR (Optical Character Recognition) abilities of the new Anthropic Claude 3 models which are vision capable. Right now it can be used to upload and convert a handwritten or digital document in pdf format to markdown.

## Why Claude 3?
The Claude 3 family of models come in 3 different sizes: Opus, Sonnet, and Haiku. All of them support prompting with images and especially Sonnet and Haiku come at a very cheap pricing compared to other vision capable large language models like GPT4-Turbo.
The main motivator for creating this demo was a post by Anthropic themselves: [Claude 3 Haiku turns thousands of physical documents into structured data](https://www.youtube.com/watch?v=RcgV2u9Kxh0)

# Usage
Dependencies are managed by [Poetry](https://python-poetry.org/docs/). See their documentation for installation.

Step 1: Clone the repository
```bash
git clone https://github.com/makefinks/note-it.git;
cd note-it
```
Step 2: Install dependencies and activate poetry environment
```bash
poetry install;
poetry shell
```
Step 3: Start the application
```bash
cd note_it/frontend/; 
python -m streamlit run upload.py
```

# Limitations
The quality of the output can vary depending on the type of document. Languages other than english will work but my testing was mostly done with english documents (handwritten and digital). At a certain point when the font or characters are to small the model will refuse to output the full text or anything at all. Furthermore, while the model will try to reconstruct tables and diagrams in markdown syntax the results are often poor.

As with every LLM Approach you need to carefully check the generated output for mistakes.

# Images
![Upload](img/upload.png)

![split_view](img/split_view.png)
