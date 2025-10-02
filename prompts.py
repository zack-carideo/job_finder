#!/usr/bin/env python3
"""
prompts used to faciliate 
updating of CV and Resume
"""


def generate_system_prompt() -> str:
    """
    Generates a system prompt for an AI model to act as a resume and cover letter customizer.

    Returns:
        str: The system prompt for the AI model.
    """
    return (
        "You are a resume and cover letter customizer. Your task is to take job postings "
        "and create customized application materials. "
        "You will be provided with job descriptions, company information, and applicant details. "
        "Use this information to tailor resumes and cover letters that align with the specific "
        "job requirements and culture of each company."
    )


def generate_resume_prompt(
    JOB_DESCRIPTION: str,
    COMPANY_INFORMATION: str,
    APPLICANT_RESUME: str
) -> str:
    """
    Generates a tailored resume for a specific job posting using the applicant's resume,
    job description, and company information.

    Args:
        job_description (str): The job posting details.
        company_information (str): Information about the company.
        applicant_resume (str): The applicant's resume.

    Returns:
        str: The prompt for generating a customized resume.
    """
    prompt = f"""You are an expert resume writer specializing in crafting resumes for 
    Data Science Managers working within enterprise functions for a financial institution. 
    Your task is to write a tailored resume for a specific job posting. 
    You will have the applicants resume, and the job posting details to inform the resume. 
    Follow these steps carefully:
    
    1. Review the job description and company information:
    <job_description>
    {JOB_DESCRIPTION}
    </job_description>

    <company_information>
    {COMPANY_INFORMATION}
    </company_information>

    2. Review the applicant's resume:
    <applicant_resume>
    {APPLICANT_RESUME}
    </applicant_resume>

    3. Analyze the job description and company information:
    - Identify key requirements for the job position
    - Note the company's core values
    - Highlight any specific skills or experiences emphasized in the job posting

    4. Analyze the applicant's resume:
    - Identify relevant experiences and qualifications that match the job requirements
    - Highlight unique achievements or skills that set the applicant apart
    - Ensure that the applicants management and leadership skills are highlighted. 

    5. Craft a tailored resume:
    - Use a clear and professional format
    - Start with a strong summary statement that aligns with the job position
    - Organize work experience in reverse chronological order, emphasizing relevant roles
    - Use bullet points to detail responsibilities and achievements, quantifying results where possible
    - Include relevant skills, certifications, and education that match the job requirements
    - Keep the same formatting style as the original resume

    6. Follow this structure for the resume, ensuring it fits on at most 2 pages:
    - Contact Information
    - Summary Statement (2-3 sentences)
    - Work Experience (most recent first)
    - Skills
    - Education
    - Certifications (if applicable)

    7. Review and refine the resume:
    - Ensure all key points from the job description are addressed

    8. Output the final resume:
    - Write the complete resume within <resume> tags, formatted as it would appear in a formal document.

    Remember to maintain the applicant's voice and style while elevating the content to match the position being applied for. 
    The resume should be concise, compelling, and tailored specifically to the company and position described, but do not 
    over embellish information that is not present in the original resume.
    """

def generate_cover_letter_prompt(
    JOB_DESCRIPTION: str,
    COMPANY_INFORMATION: str,
    APPLICANT_RESUME: str,
    APPLICANT_PREVIOUS_COVER_LETTER: str
) -> str:
    """
    Generates a tailored cover letter for a specific job posting using the applicant's resume,
    previous cover letter, job description, and company information.

    Args:
        job_description (str): The job posting details.
        company_information (str): Information about the company.
        applicant_resume (str): The applicant's resume.
        previous_cover_letter (str): The applicant's previous cover letter.

    Returns:
        str: The prompt for generating a customized cover letter.
    """

    prompt = f"""You are an expert cover letter writer specializing in crafting cover letters for Data Science Managers working within enterprise functions for a financial institution. Your task is to write a tailored cover letter for a specific job posting. You will have the applicants resume, and the job posting details to inform the cover letter. Follow these steps carefully:
    1. Review the job description and company information:
    <job_description>
    {JOB_DESCRIPTION}
    </job_description>

    <company_information>
    {COMPANY_INFORMATION}
    </company_information>

    2. Review the applicant's resume and previous cover letter:
    <applicant_resume>
    {APPLICANT_RESUME}
    </applicant_resume>

    <previous_cover_letter>
    {APPLICANT_PREVIOUS_COVER_LETTER}
    </previous_cover_letter>

    3. Analyze the job description and company information:
    - Identify key requirements for the job position
    - Note the company's core values
    - Highlight any specific skills or experiences emphasized in the job posting

    4. Analyze the applicant's resume and previous cover letter:
    - Identify relevant experiences and qualifications that match the job requirements
    - Note the applicant's writing style and tone from their previous cover letter
    - Highlight unique achievements or skills that set the applicant apart
    - Ensure that the applicants management and leadership skills are highlighted. 

    5. Craft a tailored cover letter:
    - Address the letter to the appropriate person or department
    - Open with a strong, attention-grabbing introduction
    - Align the applicant's qualifications with the positions requirements 
    - Demonstrate knowledge of the company and enthusiasm for the position
    - Use specific examples from the applicant's experience to illustrate their suitability
    - Maintain a professional yet personable tone throughout

    6. Follow this structure for the cover letter, the cover letter must fit on a single page:
    - Introduction (1 paragraph)
    - Body (2 paragraphs)
    - Conclusion (1 paragraph)

    7. Review and refine the cover letter:
    - Ensure all key points from the job description are addressed
    - Check that the companies values and core job responsibilities are reflected
    - Verify that the applicant's strengths are effectively communicated 
    - Proofread for grammar, spelling, and punctuation errors

    8. Output the final cover letter:
    Write the complete cover letter within <cover_letter> tags, formatted as it would appear in a formal document.

    Remember to maintain the applicant's voice and style while elevating the content to match the position being applied for. The cover letter should be concise, compelling, and tailored specifically to the company and position described.
    """
    return prompt
