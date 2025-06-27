from dotenv import load_dotenv

load_dotenv()
import json
import streamlit as slt
import re
from tools import draw_score,convert2img
from model.model import get_gemini_response

slt.set_page_config(page_title="ATS system")
slt.header("ATS data extraction")
job_desc=slt.text_area("Job Description",key="input")
pdf_file=slt.file_uploader(label="upload your file",type=["pdf"])
if pdf_file is not None:
    slt.write("Resume Uploaded Successfully")

submit1 = slt.button("Tell Me About the Resume")
submit2= slt.button("Percentage Match")
submit3= slt.button("Generate Cover letter")

#To make sure the button are perfectly aligned
slt.markdown(
    """
    <style>
      div[data-testid="stButton"] > button {
        display: inline-block;         
          width: 100%;          
          white-space: nowrap ;      
            overflow: hidden;                  
          text-overflow: ellipsis;          
             
      }
    </style>
    """,
    unsafe_allow_html=True
)


input_prompt1 = """
 You are an experienced Human Resource Manager with Technical Experience in the field of any one job role from Data Science or Artificial Intelligence or Machine Learning or Full Stack web development or Big Data Engineering or DEVOPS or Data Analyst, your task is to review the provided resume against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
Hey Act Like a skilled or very experience ATS(Application Tracking System) with a deep understanding of any one job role Data Science, Artificial Intelligence, Machine Learning, Full Stack web development, Big Data Engineering, DEVOPS, Data Analyst. 
Your task is to evaluate the resume based on the given job description.You must consider the job market is very competitive and you should provide best assistance for improving thr resumes. Assign the percentage Matching based on Jd and the missing keywords with high accuracy.you need to provide just the keywords for missing keywords nothing else.
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

input_prompt3 = """
Act as a seasoned HR manager and technical writer experienced in Data Science, AI, ML, Full-Stack Development, Big-Data Engineering, DevOps, and Data Analysis. Using only the candidate’s resume and the job description, create a polite, professional cover letter of about 250-300 words, structured in exactly three paragraphs. Open with a brief statement of interest and total years of relevant experience. Devote the second paragraph to matching the job’s key requirements with the candidate’s most relevant, quantified skills and achievements, explicitly noting that these abilities will be brought to the new role. End with a short closing that thanks the reader, invites further discussion, and—if the job description includes a location—adds that the candidate is willing to relocate. Write in first-person singular, active voice, simple English, avoid jargon and special symbols, and output only the final cover-letter text with no extra commentary or code.
"""


if submit1:
    if pdf_file is not None:
        pdf_bytes=convert2img.upload(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt1)
        slt.subheader("The Response is")
        slt.write(response)
    else:
        slt.write("please provide the resume")

elif submit2:
    if pdf_file is not None:
        #converting pdf to image as it is easier to understand instead of using json file s
        pdf_bytes=convert2img.upload(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt2)
        left, right = slt.columns([1, 3])
        clean_resp = response.strip()
        # removing ``` as it is produced in response by gemini 
        if clean_resp.startswith("```"):
            clean_resp = re.sub(r"^```[a-zA-Z]*\n", "", clean_resp, count=1)
            clean_resp = re.sub(r"\n```$", "", clean_resp, count=1)
        response=clean_resp
        #reading that obtained json 
        try:                                       
            data = json.loads(response)
        except json.JSONDecodeError:       
            import ast
            data = ast.literal_eval(response)

        score            = int(str(data["JD Match"]).strip("%"))
        missing_keywords = data.get("MissingKeywords", [])
        profile_summary  = data.get("Profile Summary", "")
        with left:
            #creating the score board
            slt.subheader("Match Score")        
            slt.pyplot(draw_score.draw(score))
            slt.subheader(f"score {score}/100")              
        with right:                  
            slt.subheader("Missing Keywords / Skills")
            #plotting keywords three in a column
            if missing_keywords:
                for i in range(0, len(missing_keywords), 3):
                    cols = slt.columns(3)        
                    for col, kw in zip(cols, missing_keywords[i:i + 3]):
                        with col:
                            slt.button(kw, key=kw, disabled=True)
            else:
                slt.success("Great job! No major gaps detected.")
        slt.markdown("---")     
        slt.subheader("Profile Summary")
        slt.write(profile_summary)
    else:
        slt.write("please provide the resume")        


elif submit3:
    if pdf_file is not None:
        pdf_bytes=convert2img.upload(pdf_file)
        response=get_gemini_response(job_desc,pdf_bytes,input_prompt3)
        slt.subheader("Cover Letter")
        slt.write(response)
    else:
        slt.write("please provide the resume")      