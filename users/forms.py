from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    whatsapp = forms.CharField(
        max_length=15,
        required=True,
        help_text='Enter your 10-digit WhatsApp number'
    )
    branch = forms.ChoiceField(
        choices=[
            ('', 'Select your branch/domain'),
            ('cse', 'Computer Science'),
            ('it', 'Information Technology'),
            ('ece', 'Electronics & Communication'),
            ('eee', 'Electrical & Electronics'),
            ('mech', 'Mechanical'),
            ('civil', 'Civil'),
            ('ai_ml', 'AI & Machine Learning'),
            ('cyber_security', 'Cyber Security'),
            ('data_science', 'Data Science'),
            ('other', 'Other')
        ],
        required=True
    )
    github = forms.URLField(
        required=False,
        help_text='Your GitHub profile URL'
    )
    resume = forms.FileField(
        required=False,
        help_text='Upload your resume (PDF, DOC, DOCX, max 5MB)',
        widget=forms.FileInput(attrs={'accept': '.pdf,.doc,.docx'})
    )
    additional_info = forms.CharField(
        widget=forms.Textarea,
        required=False,
        help_text='Any additional information you\'d like to share'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if not whatsapp.isdigit() or len(whatsapp) != 10:
            raise forms.ValidationError('Please enter a valid 10-digit WhatsApp number')
        return whatsapp

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create or update user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.whatsapp = self.cleaned_data['whatsapp']
            profile.branch = self.cleaned_data['branch']
            profile.github = self.cleaned_data['github']
            profile.additional_info = self.cleaned_data['additional_info']
            
            # Handle file upload
            if 'resume' in self.files:
                profile.resume = self.files['resume']
                
            profile.save()
        return user
