


prompt_json_data={
    "Data_extraction_prompt": """You are a highly skilled language model designed to extract structured data from unstructured text. Your task is to analyze the provided resume text and extract relevant information, outputting it in JSON format.

The JSON should include the following fields, setting them to `null` if no data is available:
- Name
- Contact Information (Email, Phone Number, Address)
- Professional Summary
- Education (Degree, Institution, Graduation Year)
- Work Experience (Job Title, Company, Start Date, End Date, Responsibilities)
- Soft Skills
- Hard Skills
- Certifications (if any)
- Projects (if any)
- Languages (if any)
- Awards (if any)

Here is an example of the desired JSON output format:

```json
{
  "name": "John Doe",
  "contact_information": {
    "email": "john.doe@example.com",
    "phone_number": "123-456-7890",
    "address": "123 Main St, Anytown, USA"
  },
  "professional_summary": "Experienced software engineer with a passion for developing innovative programs that expedite the efficiency and effectiveness of organizational success. Well-versed in technology and writing code to create systems that are reliable and user-friendly.",
  "education": [
    {
      "degree": "B.S. in Computer Science",
      "institution": "Anytown University",
      "graduation_year": 2020
      "CGP":"70"%
    }
  ],
  "work_experience": [
    {
      "job_title": "Software Engineer",
      "company": "Tech Solutions Inc.",
      "start_date": "January 2021",
      "end_date": "Present",
      "responsibilities": "Developed and maintained web applications, collaborated with cross-functional teams, and optimized performance."
    }
  ],
  "hard skills": [
    "Python",
    "JavaScript",
    "HTML/CSS",
    "React"
  ],
    "soft skills": [
    "Leadership ",
    "Hardworker"
  ],
  "certifications": [
    {
      "name": "Certified Kubernetes Administrator",
      "institution": "CNCF",
      "year": 2021
    }
  ],
  "projects": [
    {
      "name": "Personal Finance Tracker",
      "description": "A web application to track personal expenses and income.",
      "technologies": [
        "React",
        "Node.js",
        "MongoDB"
      ]
    }
  ],
  "languages": [
    "English",
    "Spanish"
  ],
  "awards": [
    {
      "name": "Employee of the Month",
      "institution": "Tech Solutions Inc.",
      "year": 2022
    }
  ]
}

If any of the above fields are not present in the resume, set their value to `null`. For example:

```json
{
  "name": null,
  "contact_information": {
    "email": null,
    "phone_number": null,
    "address": null
  },
  "professional_summary": null,
  "education": null,
  "work_experience": null,
  "hard skills": null,
  "soft skills":null,
  "certifications": null,
  "projects": null,
  "languages": null,
  "awards": null
}

Analyze the following resume text and produce a JSON object in the format specified above:
""",
    "Data_Rephrase_prompt":"You are tasked with rephrasing the content from a given resume content in json format to align it with a provided job description. Your goal is to optimize the resume for Applicant Tracking Systems (ATS) by ensuring it contains relevant keywords and phrases from the job description. The output should be formatted as a JSON object representing the best ATS-optimized resume.",
    "Data_Accuracy_prompt":"You are an intelligent language model designed to evaluate the accuracy and relevance of a resume in relation to a given job description. Your task is to compare the skills listed in the resume with the required skills outlined in the job description, and then provide an accuracy score and list any missing skills.Example Output:{percentage': 75,'missing_skills': ['Python', 'JavaScript'],'missing_keywords': ['Data Analysis', 'Machine Learning']}"
}

job_json=[
    {
        "jobname": "Data Analyst",
        "description": "We are looking for a Data Analyst to join our team. You will be responsible for analyzing data to help us improve our products and services. You should have strong analytical skills and be able to work with large datasets. Proficiency in SQL, Excel, and statistical software is preferred."
    },
    {
        "jobname": "Software Engineer",
        "description": "We are hiring a Software Engineer to develop software solutions. You will work with a team of developers to design and implement software applications. Candidates should have a strong understanding of programming languages such as Python, Java, or C++. Experience with web development frameworks and database management systems is a plus."
    },
    {
        "jobname": "Marketing Manager",
        "description": "We are seeking a Marketing Manager to lead our marketing team. You will develop and implement marketing strategies to promote our products and services. Candidates should have a proven track record in marketing, excellent communication skills, and the ability to manage a team."
    },
 
  ]

resume_template=[{"template_id":1,"template_name":"simple","path":"images/resume1.png"},
                 {"template_id":2,"template_name":"simple","path":"images/topics/undraw_Remote_design_team_re_urdx.png"},
                 {"template_id":3,"template_name":"simple","path":"images/topics/undraw_Remote_design_team_re_urdx.png"}  
                 ]

