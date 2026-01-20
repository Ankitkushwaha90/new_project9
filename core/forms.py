from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message', 'priority']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-0 px-4 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 transition-all duration-200',
                'placeholder': 'John Doe',
                'autocomplete': 'name',
                'aria-label': 'Full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full rounded-lg border-0 px-4 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 transition-all duration-200',
                'placeholder': 'you@example.com',
                'autocomplete': 'email',
                'aria-label': 'Email address',
                'spellcheck': 'false'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'block w-full rounded-lg border-0 px-4 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 transition-all duration-200',
                'placeholder': 'How can we help you today?',
                'aria-label': 'Subject',
                'autocomplete': 'off'
            }),
            'message': forms.Textarea(attrs={
                'class': 'block w-full rounded-lg border-0 px-4 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 transition-all duration-200',
                'rows': 4,
                'placeholder': 'Type your message here...',
                'aria-label': 'Your message',
                'spellcheck': 'true'
            }),
            'priority': forms.Select(attrs={
                'class': 'block w-full rounded-lg border-0 pl-4 pr-10 py-3 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6 appearance-none',
                'style': 'background-image: url("data:image/svg+xml,%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'none\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%236b7280\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); background-position: right 0.75rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em;',
                'aria-label': 'Message priority',
                'onchange': 'const select = this; const icon = select.value === "urgent" ? "%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'%23DC2626\' viewBox=\'0 0 24 24\'%3e%3cpath d=\'M12 2L1 21h22L12 2zm0 3.5L18.5 19h-13L12 5.5z\'/%3e%3cpath d=\'M12 16.5a1.2 1.2 0 110 2.4 1.2 1.2 0 010-2.4zm0-8.5a1 1 0 011 1v5a1 1 0 11-2 0V9a1 1 0 011-1z\'/%3e%3c/svg%3e" : (select.value ? "%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'%2310B981\' viewBox=\'0 0 24 24\'%3e%3cpath d=\'M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z\'/%3e%3c/svg%3e" : "%3csvg xmlns=\'http://www.w3.org/2000/svg\' fill=\'%236b7280\' viewBox=\'0 0 20 20\'%3e%3cpath stroke=\'%236b7280\' stroke-linecap=\'round\' stroke-linejoin=\'round\' stroke-width=\'1.5\' d=\'M6 8l4 4 4-4\'/%3e%3c/svg%3e"); select.style.backgroundImage = `url("data:image/svg+xml,${icon}")`;',
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['priority'].empty_label = 'Select priority'
