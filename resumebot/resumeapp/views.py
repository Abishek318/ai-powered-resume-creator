from django.shortcuts import render, redirect
from .forms import JobDescriptionForm
from .models import Resume,AccuracyRsesult,AnalyzedContent,JobDescription
import uuid
from dotenv import load_dotenv
import os
import google.generativeai as genai
import re 
import json
import logging
from .prompt import prompt_json_data,job_json,resume_template
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from django.urls import reverse
from .document_handler import read_pdf,word_bytes_to_pdf_base64,create_word_document
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import io

logger = logging.getLogger()
logger.setLevel(logging.INFO)

promt_path="prompt.json"
pattern = r'```json([\s\S]*?)```'

load_dotenv(".env")
GOOGLE_API_KEY=os.environ["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model_name="gemini-1.5-flash"


def home(request):    
    return render(request, 'index.html',{"template":resume_template})


def login_view(request):
    if not(request.user.is_authenticated):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.success(request, f'Welcome back, {username}!')
                    return redirect('clear_data')  
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('clear_data')  

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def upload_resume(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        template_id = request.POST.get('template_id')
        if file or template_id:
            if file:
                content=read_pdf(file)
                temp_id = str(uuid.uuid4())
                json_output= llm_model(prompt_json_data["Data_extraction_prompt"],content)
                Resume.objects.create(temp_id=temp_id, content=json.dumps(json_output),template_id=template_id)
                
                # Store temp_id in session
                request.session['temp_id'] = temp_id
            else:
                temp_id = request.session.get('temp_id')
                try:
                    resume=Resume.objects.get(temp_id=temp_id)
                    resume.template_id =template_id
                    resume.save()
                except Resume.DoesNotExist:
                    Resume.objects.create(temp_id=temp_id, content=json.dumps({}),template_id=template_id)
            if template_id:
                result_url = '/show_resume/' 
            else:
                result_url = '/analyze_description/'  
            return JsonResponse({'redirect_url': result_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def show_resume(request):
    temp_id = request.session.get('temp_id')
    if temp_id:
        resume = Resume.objects.get(temp_id=temp_id)
        if resume.template_id:
            resume=json.loads(resume.content)
            return render(request, 'show-resume.html', {'resume': resume})
        else:
            context={"page":"template_detail",'template_id': "0","page_name":"Template Selection page","message":"Sorry, you cann't view the page.First you need to select the template"}
            return  render(request, 'error_page.html', context)
    else:
        context={"page":"home","page_name":"Return to Homepage","message":"Sorry, you cann't view the page.First you need to upload the resume."}
        return  render(request, 'error_page.html', context)
    

def analyze_description(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST)
        if form.is_valid():
            temp_id = request.session.get('temp_id')
            description = form.cleaned_data['description']
            analysis_type = form.cleaned_data['analysis_type']
            try:
                job_description_content=JobDescription.objects.get(temp_id=temp_id)
                job_description_content.description =description
                job_description_content.save()

            except JobDescription.DoesNotExist:
                JobDescription.objects.create(temp_id=temp_id, description=description)


            input_text="""-resume content:{resume} 
                        -job description :{description}
            """
            if analysis_type == 'analyze':
                resume= AnalyzedContent.objects.get(temp_id=temp_id)
                
                analysis_result = llm_model(prompt_json_data["Data_Rephrase_prompt"],input_text.format(resume=resume.content,description=description))
                # Update existing object with new content
                resume.content = json.dumps(analysis_result)
                resume.save()
                return render(request, 'show-resume.html', {'resume': analysis_result})

            elif analysis_type == 'accuracy':
                resume = Resume.objects.get(temp_id=temp_id)
                analysis_result = llm_model(prompt_json_data["Data_Accuracy_prompt"],input_text.format(resume=resume.content,description=description))
                
                if AccuracyRsesult.objects.filter(temp_id = temp_id):
                    AccuracyRsesult.objects.filter(temp_id = temp_id).update(result = json.dumps(analysis_result))
                else:
                    AccuracyRsesult.objects.create(temp_id=temp_id, result=json.dumps(analysis_result))
                return redirect("result")
    else:
        form = JobDescriptionForm()
    return render(request, 'jop-des.html', {'form': form,"jobdesp":job_json,"analysis_type":"accuracy"})

def result_view(request):
    try:
        temp_id = request.session.get('temp_id')
        result_rseponse = AccuracyRsesult.objects.get(temp_id=temp_id)
        result_data=json.loads(result_rseponse.result)
        return render(request, 'result.html', result_data)
    except Exception as e:
        return redirect("home")


def job_description(request):      
     
    temp_id = request.session.get('temp_id')
    if temp_id:
        input_text="""-resume content:{resume} 
                            -job description :{description}
                """
        try:
            description=JobDescription.objects.get(temp_id=temp_id)
        except JobDescription.DoesNotExist:
            description=None
        
        if description:
            resume= AnalyzedContent.objects.get(temp_id=temp_id)

            if resume.rephrase_status==False:
                analysis_result = llm_model(prompt_json_data["Data_Rephrase_prompt"],input_text.format(resume=resume.content,description=description.description))
                # Update existing object with new content
                resume.content = json.dumps(analysis_result)
                resume.rephrase_status=True
                resume.save()
            else:
                analysis_result =json.loads(resume.content)
            return render(request, 'show-resume.html', {'resume':analysis_result })
        form = JobDescriptionForm()
        return render(request, 'jop-des.html', {'form': form,"jobdesp":job_json,"analysis_type":"analyze"})
    else:
        return redirect("home")

def template_detail(request, template_id):
        try:
            resume_upload_status=False
            temp_id = request.session.get('temp_id')
            resume = Resume.objects.get(temp_id=temp_id)
            if json.loads(resume.content):
                resume_upload_status=True
        except Exception as e:
            resume_upload_status=False
            print(e)
        if template_id:
            context = {
                'template_id': template_id,
                "resume_upload_status":resume_upload_status
            }
            return render(request, 'chose-build-method.html', context)
        else:
            context = {
                'template': resume_template,
                "resume_upload_status":resume_upload_status
            }
            return render(request, 'resume-templates.html', context)
            

def store_resume(request):
    if request.method == 'POST':
        # Retrieve POST data
        data = json.loads(request.body.decode('utf-8'))
        resume_data = data.get('resume', {})  # Get the 'resume' object from the JSON data

        # Construct the JSON structure
        formatted_resume = {
            "name": resume_data.get("name", ""),
            "contact_information": resume_data.get("contact_information", {}),
            "professional_summary": resume_data.get("professional_summary", ""),
            "education": resume_data.get("education", []),
            "work_experience": resume_data.get("work_experience", []),
            "hard_skills": resume_data.get("hard_skills", []),
            "soft_skills": resume_data.get("soft_skills", []),
            "certifications": resume_data.get("certifications", []),
            "projects": resume_data.get("projects", []),
            "languages": resume_data.get("languages", []),
            "awards": resume_data.get("awards", [])
        }

        temp_id = request.session.get('temp_id')
        resume_json = json.dumps(formatted_resume)

        try:
            analyzed_content = AnalyzedContent.objects.get(temp_id=temp_id)
            analyzed_content.content = resume_json
            analyzed_content.rephrase_status=False
            analyzed_content.save()
        except AnalyzedContent.DoesNotExist:
            AnalyzedContent.objects.create(temp_id=temp_id, content=resume_json)

        return JsonResponse({
            'status': 'success',
            'message': 'Resume stored successfully',
            'redirect_url': reverse('job_description') 
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def resume_preview(request):
    temp_id = request.session.get('temp_id')
    if temp_id:
        try:
            analyzed_content = AnalyzedContent.objects.get(temp_id=temp_id)
        except AnalyzedContent.DoesNotExist:
            analyzed_content=Resume.objects.get(temp_id=temp_id)

        if analyzed_content:
            doc = create_word_document(json_data=json.loads(analyzed_content.content))
            # Convert Document object to bytes
            docx_bytes = io.BytesIO()
            doc.save(docx_bytes)
            docx_bytes = docx_bytes.getvalue()
            
            pdf_base64 = word_bytes_to_pdf_base64(docx_bytes,temp_id)
            context = {"resume_doc_byte": pdf_base64}
            return render(request, 'resume_preview.html', context)
        return render(request, 'resume_preview.html', context)
    else:
        return redirect("home")

def create_new_resume(request):
    if request.method == 'POST':
        temp_id = str(uuid.uuid4())
        request.session['temp_id'] = temp_id
        template_id = request.POST.get('template_id')
        Resume.objects.create(temp_id=temp_id, content=json.dumps({}),template_id=template_id)
        context={'resume': {}}
        return render(request, 'show-resume.html', context)
    redirect("home")
   

@login_required
def clear_data(request):
    # Get counts of data in each model
    context = {
        'models': [
            {'model_name': 'Resume', 'count': Resume.objects.count()},
            {'model_name': 'AnalyzedContent', 'count': AnalyzedContent.objects.count()},
            {'model_name': 'AccuracyRsesult', 'count': AccuracyRsesult.objects.count()},
            {'model_name': 'JobDescription', 'count': JobDescription.objects.count()},
        ]
    }

    if request.method == 'POST':
        # Handle POST request to truncate all models
        Resume.objects.all().delete()
        AnalyzedContent.objects.all().delete()
        AccuracyRsesult.objects.all().delete()
        JobDescription.objects.all().delete()
        return redirect('clear_data')  # Redirect to clear_data page after truncating

    return render(request, 'clear_data.html', context)
# def download_resume(request, session_id):
#     file_path = os.path.join(settings.MEDIA_ROOT, 'temp', session_id, 'resume.pdf')
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/pdf")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     return HttpResponse("File not found", status=404)


# ++++++++++++++++++++++++++++++++++++


def llm_model(system_prompt:str,resume_text:str):

    llm = genai.GenerativeModel(model_name,system_instruction=[system_prompt])
    response = llm.generate_content(resume_text)

    logger.info(response.text)
    match = re.search(pattern, response.text)
    if match:
        # Extract JSON data from the first capturing group
        json_data = match.group(1)

        # Parse JSON data
        try:
            parsed_data = json.loads(json_data)
        except:
            parsed_data = json.loads(json_data.replace("'",'"'))
    else:
        parsed_data={}
    return parsed_data


