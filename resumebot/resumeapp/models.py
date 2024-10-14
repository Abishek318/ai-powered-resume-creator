from django.db import models

# Create your models here.

class AccuracyRsesult (models.Model):
    temp_id = models.CharField(max_length=100, unique=True)
    result = models.TextField()

    def __str__(self):
        return self.temp_id
    
class Resume(models.Model):
    temp_id = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    template_id=models.TextField(null=True,blank=True)

    def __str__(self):
        return self.temp_id
    
class JobDescription(models.Model):
    temp_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()

class AnalyzedContent(models.Model):
    temp_id = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    rephrase_status = models.BooleanField(default=False)

# class ResumeDocument(models.Model):
#     temp_id = models.CharField(max_length=100, unique=True)
#     pdf = models.FileField(upload_to='pdfs/',null=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.temp_id