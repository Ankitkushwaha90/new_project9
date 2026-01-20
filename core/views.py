from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from services.api_client import api_client
import logging

logger = logging.getLogger(__name__)

def home(request):
    """
    Home page - display featured courses from backend API
    """
    # Get some featured courses to display on home page
    courses_data = api_client.get_courses({'page_size': 6})  # Get first 6 courses
    featured_courses = []
    
    if courses_data and 'results' in courses_data:
        featured_courses = courses_data['results']
    
    return render(request, 'core/home.html', {
        'featured_courses': featured_courses
    })

@login_required
def dashboard(request):
    """
    User dashboard - display user progress from backend API
    """
    user_progress = []
    recent_courses = []
    
    # Try to get user progress from backend API
    if request.user.is_authenticated:
        # First authenticate with backend API using user credentials
        # Note: In a real implementation, you'd want to handle this more securely
        progress_data = api_client.get_user_progress()
        if progress_data and 'results' in progress_data:
            user_progress = progress_data['results']
    
    # Get recent courses
    courses_data = api_client.get_courses({'page_size': 5})
    if courses_data and 'results' in courses_data:
        recent_courses = courses_data['results']
    
    return render(request, 'core/dashboard.html', {
        'user_progress': user_progress,
        'recent_courses': recent_courses
    })

def about(request):
    return render(request, 'core/about.html')

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from .models import Contact

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact form data
            contact = form.save(commit=False)
            contact.save()
            
            # Send email notification (optional)
            try:
                send_mail(
                    f'New Contact Form Submission: {contact.subject}',
                    f'Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't show it to the user
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f'Error sending contact email: {str(e)}')
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        # Pre-fill the form with GET parameters if they exist
        initial_data = {
            'name': request.GET.get('name', ''),
            'email': request.GET.get('email', ''),
            'subject': request.GET.get('subject', ''),
            'message': request.GET.get('message', ''),
            'priority': request.GET.get('priority', 'medium'),
        }
        form = ContactForm(initial=initial_data)
    
    return render(request, 'core/contact.html', {'form': form})


def freelance_listings(request):
    # Sample freelance gigs (replace with DB model later)
    gigs = [
        {
            'title': 'Build a Custom Pentesting Dashboard',
            'client': 'CyberCorp Inc.',
            'budget': '$1,200 – $1,800',
            'skills': ['Python', 'Flask', 'Burp Suite', 'Docker'],
            'deadline': 'Nov 25, 2025',
            'posted': '2 days ago',
            'verified': True,
        },
        {
            'title': 'AI-Powered Phishing Detection Tool',
            'client': 'SecureMind AI',
            'budget': '$2,500',
            'skills': ['PyTorch', 'NLP', 'FastAPI', 'AWS'],
            'deadline': 'Dec 10, 2025',
            'posted': '1 week ago',
            'verified': True,
        },
        {
            'title': 'WordPress Hardening & Malware Cleanup',
            'client': 'BlogWave Media',
            'budget': '$350',
            'skills': ['WordPress', 'Security', 'PHP'],
            'deadline': 'Nov 18, 2025',
            'posted': '3 days ago',
            'verified': False,
        },
        {
            'title': 'Reverse Engineering Malware Sample',
            'client': 'ThreatLab Research',
            'budget': '$800 – $1,200',
            'skills': ['Ghidra', 'x64dbg', 'Assembly', 'C++'],
            'deadline': 'Nov 30, 2025',
            'posted': '5 days ago',
            'verified': True,
        },
    ]

    context = {
        'gigs': gigs,
        'total_gigs': len(gigs),
        'page_title': 'Freelance Cyber Gigs',
    }
    return render(request, 'core/freelance.html', context)


def search(request):
    """
    Search functionality using backend API
    """
    query = request.GET.get('q', '')
    results = []
    
    if query:
        # Search courses using backend API
        search_params = {
            'search': query,
            'page_size': 20
        }
        courses_data = api_client.get_courses(search_params)
        if courses_data and 'results' in courses_data:
            results = courses_data['results']
    
    return render(request, 'core/search.html', {
        'query': query,
        'results': results
    })

def api_login(request):
    """
    Handle login and authenticate with backend API
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            # First authenticate with Django
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                
                # Then authenticate with backend API
                if api_client.authenticate(username, password):
                    messages.success(request, 'Successfully logged in and connected to backend API!')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'Logged in locally but failed to connect to backend API.')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'registration/login.html')

# courses/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def lab_setup_view(request):
    """Main lab setup page"""
    return render(request, 'lab_setup/lab_setup.html')

def lab_tools_library(request):
    """Library of cybersecurity tools"""
    tools = [
        {
            'name': 'Kali Linux',
            'category': 'OS',
            'description': 'Pre-installed pentesting distribution',
            'download': 'https://www.kali.org/get-kali/',
            'install': 'VM or dual-boot',
            'icon': 'fab fa-linux',
        },
        {
            'name': 'Burp Suite',
            'category': 'Web',
            'description': 'Web vulnerability scanner',
            'download': 'https://portswigger.net/burp',
            'install': 'Download + Java',
            'icon': 'fas fa-bug',
        },
        {
            'name': 'Wireshark',
            'category': 'Network',
            'description': 'Network protocol analyzer',
            'download': 'https://www.wireshark.org/',
            'install': 'Native installer',
            'icon': 'fas fa-network-wired',
        },
        {
            'name': 'Metasploit',
            'category': 'Exploitation',
            'description': 'Exploitation framework',
            'download': 'Pre-installed in Kali',
            'install': 'msfconsole',
            'icon': 'fas fa-bomb',
        },
        {
            'name': 'Nmap',
            'category': 'Scanning',
            'description': 'Network mapper',
            'download': 'Pre-installed',
            'install': 'nmap -sV target',
            'icon': 'fas fa-search',
        },
        {
            'name': 'Ghidra',
            'category': 'Reverse Engineering',
            'description': 'Software reverse engineering suite',
            'download': 'https://ghidra-sre.org/',
            'install': 'Java 17+',
            'icon': 'fas fa-microchip',
        },
    ]
    
    return render(request, 'lab_setup/tools.html', {'tools': tools})

@csrf_exempt
def lab_wizard(request):
    """Interactive lab setup wizard"""
    if request.method == 'POST':
        data = json.loads(request.body)
        step = data.get('step', 1)
        choice = data.get('choice', '')
        
        # Simulate wizard logic
        if step == 1:  # OS Choice
            if choice == 'kali':
                return JsonResponse({
                    'next_step': 2,
                    'content': 'Download Kali ISO from kali.org',
                    'action': 'Download ISO'
                })
            elif choice == 'parrot':
                return JsonResponse({
                    'next_step': 2,
                    'content': 'Download Parrot Security OS',
                    'action': 'Download Parrot'
                })
        
        elif step == 2:  # Installation Type
            if choice == 'vm':
                return JsonResponse({
                    'next_step': 3,
                    'content': 'Install VirtualBox or VMware',
                    'tools': ['VirtualBox', 'VMware Workstation']
                })
            elif choice == 'dual-boot':
                return JsonResponse({
                    'next_step': 3,
                    'content': 'Backup data and create bootable USB',
                    'tools': ['Rufus', 'Etcher']
                })
        
        elif step == 3:  # VM Setup
            if choice == 'virtualbox':
                return JsonResponse({
                    'next_step': 4,
                    'content': 'Create new VM with 4GB RAM, 2 cores, 50GB disk',
                    'screenshot': '/static/img/virtualbox-setup.png'
                })
        
        elif step == 4:  # Network Configuration
            return JsonResponse({
                'next_step': 5,
                'content': 'Configure NAT + Host-Only adapter for lab isolation',
                'warning': '⚠️ Never use lab network for personal browsing'
            })
        
        elif step == 5:  # Tool Installation
            return JsonResponse({
                'next_step': 6,
                'content': 'Install essential tools: nmap, metasploit, burpsuite',
                'commands': [
                    'sudo apt update',
                    'sudo apt install nmap metasploit-framework burpsuite'
                ]
            })
        
        elif step == 6:  # Lab Network
            return JsonResponse({
                'next_step': 7,
                'content': 'Set up vulnerable VMs (Metasploitable, DVWA)',
                'resources': ['https://www.vulnhub.com/']
            })
        
        elif step == 7:  # Testing
            return JsonResponse({
                'complete': True,
                'content': '🎉 Your lab is ready! Start with nmap -sV 192.168.56.101',
                'next_action': 'Launch First Scan'
            })
        
        return JsonResponse({'error': 'Invalid step'})

    # Initial wizard state
    return JsonResponse({
        'step': 1,
        'title': 'Choose Your Base OS',
        'content': 'What operating system will you use for your lab?',
        'choices': [
            {'value': 'kali', 'label': 'Kali Linux', 'icon': 'fab fa-linux'},
            {'value': 'parrot', 'label': 'Parrot Security', 'icon': 'fas fa-parrot'}
        ]
    })

@login_required
def recommendations(request):
    """
    Display personalized course recommendations for the user
    """
    # Get recommended courses (in a real app, this would be based on user's activity and preferences)
    recommended_courses = []
    try:
        # Get all courses as recommendations (in a real app, this would be filtered/ranked)
        courses_data = api_client.get_courses({'page_size': 12})
        if courses_data and 'results' in courses_data:
            recommended_courses = courses_data['results']
    except Exception as e:
        logger.error(f"Error fetching recommended courses: {str(e)}")
        messages.error(request, 'Error loading recommendations. Please try again later.')
    
    # Get user's enrolled courses to filter them out from recommendations
    enrolled_courses = []
    try:
        user_courses = api_client.get_user_courses(request.user.id)
        if user_courses and 'results' in user_courses:
            enrolled_courses = [course['id'] for course in user_courses['results']]
    except Exception as e:
        logger.error(f"Error fetching user's enrolled courses: {str(e)}")
    
    # Filter out already enrolled courses
    filtered_recommendations = [
        course for course in recommended_courses 
        if course.get('id') not in enrolled_courses
    ]
    
    return render(request, 'core/recommendations.html', {
        'recommended_courses': filtered_recommendations,
        'enrolled_courses': enrolled_courses
    })
