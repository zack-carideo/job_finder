#!/usr/bin/env python3
"""
Resume and Cover Letter Customizer
Takes job results and creates customized application materials for each job posting using AI prompts.
"""
import os, sys,  json, anthropic
from IPython.display import Markdown, display
from pathlib import Path
from urllib.parse import urlparse
#customs
from utils import load_docx_text 
from prompts import generate_system_prompt, generate_cover_letter_prompt, generate_resume_prompt
from pydantic import BaseModel, HttpUrl, AnyUrl, field_validator, FilePath
from typing import Dict, Union, List

class JobResult(BaseModel):
    job_url: str
    job_name: str
    company: str
    job_description: str
    additional_info: str
    key_requirements: dict 

    @field_validator('job_url')
    def validate_url(cls,v):
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError('Invalid URL format')
        return v
    
class resume_and_cv(BaseModel):
    resume_path: FilePath
    coverletter_path: FilePath

    @field_validator('resume_path', 'coverletter_path')
    def validate_docx_extension(cls, v):
        if not str(v).lower().endswith('.docx'):
            raise ValueError('File must be a .docx file')
        return v


def main(linked_in_results_path:dict
         , resume_path: str
         , coverletter_path: str
         ): 
    
    file_validator = resume_and_cv(
        resume_path=resume_path,
        coverletter_path=coverletter_path
    )

    #1 execute update of resume 

    #2 execute update of cover letter

    #3 return updated documents
    pass


if __name__ == "__main__":

    #root path
    _root = Path.cwd()
    linked_in_job_results_path = _root / "job_results.json"
    coverletter_path = "C:/Users/zjc10/OneDrive/Personal/Resume/CoverLetter - USAA Director AI_ML (Model Development).docx"
    resume_path = "C:/Users/zjc10/OneDrive/Personal/Resume/Zach Carideo Resume 2025 v2.docx"

    file_validator = resume_and_cv(
        resume_path=resume_path,
        coverletter_path=coverletter_path
    )

    #coverletter & resume 
    coverletter = load_docx_text(file_validator.coverletter_path)
    resume = load_docx_text(file_validator.resume_path)

    #load scrapped job details 
    with open(linked_in_job_results_path, 'r', encoding='utf-8') as f:
        jobs = json.load(f)

    _results = []
    for _d in jobs: 
        #unpack job details and validate
        job = JobResult(**_d)
        job_description = _d['job_description']
        company_information = _d['company_information']

        #generate resume prompt 
        resume_prompt = generate_resume_prompt(
            JOB_DESCRIPTION=job_description,
            COMPANY_INFORMATION=company_information,
            APPLICANT_RESUME=resume
        )

        #generate cover letter prompt 
        cover_letter_prompt = generate_cover_letter_prompt(
            JOB_DESCRIPTION=job_description,
            COMPANY_INFORMATION=company_information,
            APPLICANT_RESUME=resume,
            APPLICANT_PREVIOUS_COVER_LETTER=coverletter
        )

        #print prompts for debugging 
        display(Markdown("### Resume Prompt"))
        display(Markdown(resume_prompt))
        display(Markdown("### Cover Letter Prompt"))
        display(Markdown(cover_letter_prompt))

        #call anthropic api to get response 
        client = anthropic.Client(os.getenv("ANTHROPIC_API_KEY"))

        #get resume response 
        resume_response = client.completions.create(
            model="claude-2",
            max_tokens=2000,
            temperature=0.7,
            top_p=1,
            prompt=f"{generate_system_prompt()}\n\nHuman: {resume_prompt}\n\nAssistant:"
        )

        #get cover letter response 
        cover_letter_response = client.completions.create(
            model="claude-2",
            max_tokens=2000,
            temperature=0.7,
            top_p=1,
            prompt=f"{generate_system_prompt()}\n\nHuman: {cover_letter_prompt}\n\nAssistant:"
        )

        #print responses for debugging 
        display(Markdown("### Resume Response"))
        display(Markdown(resume_response.completion))
        display(Markdown("### Cover Letter Response"))
        display(Markdown(cover_letter_response.completion))

        _results.append({
            "job_title": _d['job_title'],
            "company_name": _d['company_name'],
            "location": _d['location'],
            "job_posting_url": _d['job_posting_url'],
            "customized_resume": resume_response.completion,
            "customized_cover_letter": cover_letter_response.completion
        })

    # Save results to JSON file
    output_file = _root / "customized_applications.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(_results, f, indent=4, ensure_ascii=False)