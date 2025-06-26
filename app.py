from dotenv import load_dotenv

load_dotenv()

import streamlit as slt
import os
from PIL.Image import Image
import pdf2image
from google import genai
from google.genai import types
import base64
import io

client = genai.Client()

def get_gemini_response(input,pdf_content,prompt):
    image_parts = [
        types.Part.from_bytes(
            data=base64.b64decode(page["data"]),
            mime_type=page["mime_type"]
        )
        for page in pdf_content
    ]
    contents = [
        prompt,                        
        f"Job Description:\n{input}",  
        *image_parts                   
    ]
    response = client.models.generate_content(
         model="gemini-2.5-flash",
        contents=contents,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_budget=0)  # disable ‘slow thinking’
        ),
    )
    return response.text

def input_pdf_setup(upload_file):
    #converting pdf to image
    file_images=pdf2image.convert_from_bytes(upload_file.read())
    pdf_parts=[]
    if file_images:
        for image in file_images:
            first_pages=image
            img_byte_arr = io.BytesIO()
            first_pages.save(img_byte_arr, format="JPEG")
            img_byte_arr=img_byte_arr.getvalue()
            pdf_parts.append({
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            })
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")


slt.set_page_config(page_title="ATS system")
slt.header("ATS data extraction")
job_desc=slt.text_area("Job Description",key="input")
pdf_file=slt.file_uploader(label="upload your file",type=["pdf"])

if pdf_file is not None:
    slt.write("Resume Uploaded Successfully")

submit1 = slt.button("Tell Me About the Resume")
submit2= slt.button("Percentage Match")
submit3= slt.button("Generate Cover letter")
input_prompt1 = """
 You are an experienced Human Resource Manager with Technical Experience in the field of any one job role from Data Science or Artificial Intelligence or Machine Learning or Full Stack web development or Big Data Engineering or DEVOPS or Data Analyst, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of any one job role Data Science, Artificial Intelligence, Machine Learning, Full Stack web development, Big Data Engineering, DEVOPS, Data Analyst. 
Your task is to evaluate the resume based on the given job description.You must consider the job market is very competitive and you should provide best assistance for improving thr resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy.
I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""
input_prompt3 = """
Act as a seasoned HR manager and technical writer experienced in Data Science, AI, ML, Full-Stack Development, Big-Data Engineering, DevOps, and Data Analysis. Using only the candidate’s resume and the job description, create a polite, professional cover letter of about 250-300 words, structured in exactly three paragraphs. Open with a brief statement of interest and total years of relevant experience. Devote the second paragraph to matching the job’s key requirements with the candidate’s most relevant, quantified skills and achievements, explicitly noting that these abilities will be brought to the new role. End with a short closing that thanks the reader, invites further discussion, and—if the job description includes a location—adds that the candidate is willing to relocate. Write in first-person singular, active voice, simple English, avoid jargon and special symbols, and output only the final cover-letter text with no extra commentary or code.
"""
if submit1:
    if pdf_file is not None:
        pdf_bytes=input_pdf_setup(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt1)
        slt.subheader("The Response is")
        slt.write(response)
    else:
        slt.write("please provide the resume")

elif submit2:
    if pdf_file is not None:
        pdf_bytes=input_pdf_setup(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt2)
        slt.subheader("The Response is")
        slt.write(response)
    else:
        slt.write("please provide the resume")        


elif submit3:
    if pdf_file is not None:
        pdf_bytes=input_pdf_setup(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt3)
        slt.subheader("Cover Letter")
        slt.write(response)
    else:
        slt.write("please provide the resume")      