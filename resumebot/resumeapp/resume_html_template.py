
template_1="""
<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ name }} - Resume</title>
        <style>
            @page {
                size: letter;
                margin: 2cm;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
                line-height: 1.4;
                color: #333;
            }
            h1 {
                font-size: 24px;
                color: #2c3e50;
                margin-bottom: 5px;
            }
            h2 {
                font-size: 16px;
                color: #2c3e50;
                margin-top: 15px;
                margin-bottom: 5px;
                border-bottom: 1px solid #2c3e50;
                padding-bottom: 3px;
            }
            .contact-info {
                font-size: 11px;
                margin-bottom: 15px;
            }
            .section {
                margin-bottom: 15px;
            }
            .job-title, .degree {
                font-weight: bold;
            }
            .company, .institution {
                font-style: italic;
            }
            ul {
                margin: 5px 0;
                padding-left: 20px;
            }
            li {
                margin-bottom: 3px;
            }
        </style>
    </head>
    <body>
        <h1>{{ name }}</h1>
        <div class="contact-info">
            <p>
                {% if contact_information.email %}Email: {{ contact_information.email }}{% endif %}
                {% if contact_information.phone_number %} | Phone: {{ contact_information.phone_number }}{% endif %}
                {% if contact_information.address %} | Address: {{ contact_information.address }}{% endif %}
            </p>
        </div>
        
        <div class="section">
            <h2>Professional Summary</h2>
            <p>{{ professional_summary }}</p>
        </div>
        
        <div class="section">
            <h2>Education</h2>
            {% for edu in education %}
            <p>
                <span class="degree">{{ edu.degree }}</span>, 
                <span class="institution">{{ edu.institution }}</span>, 
                {{ edu.graduation_year }}
            </p>
            {% if edu.CGP %}
            <p>CGP: {{ edu.CGP }}</p>
            {% endif %}
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>Work Experience</h2>
            {% for job in work_experience %}
            <p>
                <span class="job-title">{{ job.job_title }}</span>, 
                <span class="company">{{ job.company }}</span>, 
                {{ job.start_date }} - {{ job.end_date }}
            </p>
            <ul>
                {% for responsibility in job.responsibilities.split('. ') %}
                <li>{{ responsibility }}</li>
                {% endfor %}
            </ul>
            {% endfor %}
        </div>
        
        <div class="section">
            <h2>Skills</h2>
            {% if hard_skills %}
            <p><strong>Hard Skills:</strong> {{ hard_skills|join(', ') }}</p>
            {% endif %}
            {% if soft_skills %}
            <p><strong>Soft Skills:</strong> {{ soft_skills|join(', ') }}</p>
            {% endif %}
        </div>
        
        {% if certifications %}
        <div class="section">
            <h2>Certifications</h2>
            {% for cert in certifications %}
            <p>{{ cert.name }}, {{ cert.institution }}, {{ cert.year }}</p>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if projects %}
        <div class="section">
            <h2>Projects</h2>
            {% for project in projects %}
            <p><strong>{{ project.name }}:</strong> {{ project.description }}</p>
            <p>Technologies: {{ project.technologies|join(', ') }}</p>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if languages %}
        <div class="section">
            <h2>Languages</h2>
            <p>{{ languages|join(', ') }}</p>
        </div>
        {% endif %}
        
        {% if awards %}
        <div class="section">
            <h2>Awards</h2>
            {% for award in awards %}
            <p>{{ award.name }}, {{ award.institution }}, {{ award.year }}</p>
            {% endfor %}
        </div>
        {% endif %}
    </body>
    </html>
"""
html_template_json={"NXTCG7Ir4z":template_1,"YAC4nDlAB8":template_1,"gMR5oGDETm":template_1}
