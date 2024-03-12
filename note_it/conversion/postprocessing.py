import cv2

def fix_headings_rulebased(markdown_text: str):
    
    lines = markdown_text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("#"):
            words = line.split(" ")

            # remove heading annotation if lenght of words is greater than 4
            if len(words) > 5:
                ## remove heading annotation (e.g. #, ##, ###, etc.)
                lines[i] = " ".join(words[1:])

    return "\n".join(lines)

def enhance_image_otsu(image_path: str):
    # Read the image
    img = cv2.imread(image_path, 0)
    
    # Apply Otsu thresholding
    _, img = cv2.threshold(img, 
                           0, 
                           255, 
                           cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Save the image
    cv2.imwrite(f"{image_path}_corrected", img)
    print(f"Image enhanced using Otsu thresholding and saved at {image_path}_corrected")
