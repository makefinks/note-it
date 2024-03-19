import cv2

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
