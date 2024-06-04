
from fastapi import FastAPI,UploadFile
from fastapi.responses import JSONResponse
import google.generativeai as genai
from dotenv import load_dotenv
from pydantic import BaseModel
import PyPDF2 as pdf
import logging
import uvicorn
import json
import os
import re
import io

#LOGGING
logger = logging.getLogger()
logger.setLevel(logging.INFO)

promt_path="prompt.json"


load_dotenv(".env")
GOOGLE_API_KEY=os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model_name="gemini-1.5-flash"

app = FastAPI()
# json format
pattern = r'```json([\s\S]*?)```'


def input_pdf_text(contents):
    reader=pdf.PdfReader(io.BytesIO(contents))
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

# class PromptText:
#     def __init__(self, json_data):
#         for key, value in json_data.items():
#             setattr(self, key, value)

class LlmInput(BaseModel):
    input_text: str
    system_promt_name: str 


# api
@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    logger.info(file.filename)
    contents = await file.read()
    pdf_file_text=input_pdf_text(contents)
    json_output= llm_model(prompt_json_data["Data_extraction_prompt"],pdf_file_text)
    return JSONResponse(content=json_output)

# api
@app.post("/llm/")
async def llm_model_handler(llminput:LlmInput):
    logger.info(llminput)
    json_output= llm_model(prompt_json_data[llminput.system_promt_name],llminput.input_text)
    return JSONResponse(content=json_output)


def llm_model(system_prompt:str,resume_text:str):

    llm = genai.GenerativeModel(model_name,system_instruction=[system_prompt])
    response = llm.generate_content(resume_text)

    logger.info(response.text)
    match = re.search(pattern, response.text)
    if match:
        # Extract JSON data from the first capturing group
        json_data = match.group(1)

        # Parse JSON data
        parsed_data = json.loads(json_data)
    else:
        parsed_data={}
    return parsed_data

if __name__=="__main__":
    with open(promt_path,"r") as f:
        prompt_json_data = json.loads(f.read())

    # prompts=PromptText(prompt_json_data)
    uvicorn.run(app, host="0.0.0.0", port=8000)