from docx import Document
import json

paths_ = json.load(open("%s%s" % ("resources\\","paths.json")))
######################################################################################

def convert_docx_to_txt(docx_filename, txt_filename):
    # Load the Word document
    doc = Document(docx_filename)
    
    # Create or open the target .txt file
    with open(txt_filename, 'w', encoding='utf-8') as txt_file:
        for paragraph in doc.paragraphs:
            txt_file.write(paragraph.text + '\n')

# Replace these filenames with your actual file paths
docx_filename = "%s%s" % (paths_["projectDir"],".docx")
txt_filename = "%s%s" % (paths_["content"]["main"],".txt")
convert_docx_to_txt(docx_filename, txt_filename)