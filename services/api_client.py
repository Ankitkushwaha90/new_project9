import requests
import json
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

class BackendAPIClient:
    """
    Client for communicating with the backend API server
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'BACKEND_API_URL', 'http://127.0.0.1:8000')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
        })
    
    def _make_request(self, method, endpoint, data=None, params=None, auth_required=False):
        """
        Make HTTP request to backend API
        """
        # Ensure endpoint starts with /api/ if not already present
        if not endpoint.startswith('/api/'):
            endpoint = f"/api/{endpoint.lstrip('/')}"
        url = f"{self.base_url.rstrip('/')}{endpoint}"
        
        try:
            if auth_required:
                # Get token from session or cache if needed
                token = self._get_auth_token()
                if token:
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
            
            response = self.session.request(
                method=method,
                url=url,
                json=data if data else None,
                params=params
            )
            
            if response.status_code == 401 and auth_required:
                # Token might be expired, try to refresh
                if self._refresh_token():
                    # Retry the request with new token
                    token = self._get_auth_token()
                    self.session.headers.update({
                        'Authorization': f'Bearer {token}'
                    })
                    response = self.session.request(
                        method=method,
                        url=url,
                        json=data if data else None,
                        params=params
                    )
            
            response.raise_for_status()
            return response.json() if response.content else {}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def _get_auth_token(self):
        """Get authentication token from cache"""
        return cache.get('backend_api_access_token')
    
    def _set_auth_token(self, access_token, refresh_token=None):
        """Store authentication tokens in cache"""
        cache.set('backend_api_access_token', access_token, timeout=3600)  # 1 hour
        if refresh_token:
            cache.set('backend_api_refresh_token', refresh_token, timeout=86400)  # 24 hours
    
    def _refresh_token(self):
        """Refresh the access token"""
        refresh_token = cache.get('backend_api_refresh_token')
        if not refresh_token:
            return False
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/token/refresh/",
                json={'refresh': refresh_token}
            )
            response.raise_for_status()
            
            tokens = response.json()
            self._set_auth_token(tokens['access'])
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Token refresh failed: {e}")
            return False
    
    def authenticate(self, username, password):
        """
        Authenticate with backend API and store tokens
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/token/",
                json={
                    'username': username,
                    'password': password
                }
            )
            response.raise_for_status()
            
            tokens = response.json()
            self._set_auth_token(tokens['access'], tokens['refresh'])
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def get_courses(self, params=None):
        """
        Get list of courses from backend API with related blogs and subtopics
        """
        if params is None:
            params = {}
        # Include related blogs and subtopics in the response
        params['expand'] = 'blogs,blogs.subtopics'
        return self._make_request('GET', 'courses/', params=params)
    
    def get_course_detail(self, course_id):
        """
        Get detailed information about a specific course
        """
        return self._make_request('GET', f'/courses/{course_id}/')
    
    def get_course_lessons(self, course_id):
        """
        Get lessons for a specific course
        """
        return self._make_request('GET', f'/courses/{course_id}/lessons/')
    
    def get_course_quizzes(self, course_id):
        """
        Get quizzes for a specific course
        """
        return self._make_request('GET', f'/courses/{course_id}/quizzes/')
    
    def get_lesson_detail(self, lesson_id):
        """
        Get detailed information about a specific lesson
        """
        return self._make_request('GET', f'/lessons/{lesson_id}/')
    
    def get_quiz_detail(self, quiz_id):
        """
        Get detailed information about a specific quiz
        """
        return self._make_request('GET', f'/quizzes/{quiz_id}/')
    
    def get_user_progress(self):
        """
        Get user's progress (requires authentication)
        """
        return self._make_request('GET', '/progress/', auth_required=True)
    
    def update_progress(self, progress_data):
        """
        Update user progress (requires authentication)
        """
        return self._make_request('POST', '/progress/', data=progress_data, auth_required=True)
    
    def create_course(self, course_data):
        """
        Create a new course (requires admin authentication)
        """
        return self._make_request('POST', '/courses/', data=course_data, auth_required=True)


# Global instance
api_client = BackendAPIClient()