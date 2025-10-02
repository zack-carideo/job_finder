#!/usr/bin/env python3
"""
utilities to support job application agent
"""
from docx import Document

def load_docx_text(file_path):
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


## ADD GOOGLE SEARCH FUNCTIONALITY LATER (ZJC 09/25/2025)
## This will be used to help gather general company information for cover letters
def search_google():
    pass
