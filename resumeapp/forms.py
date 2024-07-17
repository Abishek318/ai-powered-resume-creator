from django import forms


class ResumeUploadForm(forms.Form):
    resume = forms.FileField()

class JobDescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label='Job Description',required=True)
    analysis_type = forms.CharField(widget=forms.Textarea, label='analysis type',required=True)



# class JobDescriptionForm(forms.Form):
#     description = forms.CharField(widget=forms.Textarea, label='Job Description')
#     analysis_type = forms.ChoiceField(
#         choices=ANALYSIS_CHOICES,
#         widget=forms.RadioSelect,
#         label='Select Analysis Type'
#     )


