class ActivityFeed {
    constructor() {
        this.activitiesContainer = document.getElementById('activities-container');
        this.filterButtons = document.querySelectorAll('[data-activity-filter]');
        this.markAllReadBtn = document.getElementById('mark-all-read');
        this.loadMoreBtn = document.getElementById('load-more-activities');
        this.currentFilter = 'all';
        this.page = 1;
        this.isLoading = false;
        
        this.initializeEventListeners();
        this.loadActivities();
    }
    
    initializeEventListeners() {
        // Filter buttons
        this.filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const filter = btn.dataset.activityFilter;
                this.setActiveFilter(btn, filter);
                this.page = 1;
                this.loadActivities();
            });
        });
        
        // Mark all as read
        if (this.markAllReadBtn) {
            this.markAllReadBtn.addEventListener('click', () => this.markAllAsRead());
        }
        
        // Load more button
        if (this.loadMoreBtn) {
            this.loadMoreBtn.addEventListener('click', () => this.loadMoreActivities());
        }
        
        // Mark as read on click
        document.addEventListener('click', (e) => {
            const markReadBtn = e.target.closest('.mark-as-read');
            if (markReadBtn) {
                e.preventDefault();
                const activityId = markReadBtn.dataset.activityId;
                this.markAsRead(activityId, markReadBtn.closest('.activity-item'));
            }
        });
    }
    
    setActiveFilter(activeBtn, filter) {
        this.filterButtons.forEach(btn => btn.classList.remove('bg-indigo-100', 'text-indigo-800'));
        activeBtn.classList.add('bg-indigo-100', 'text-indigo-800');
        this.currentFilter = filter;
    }
    
    async loadActivities() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.toggleLoading(true);
        
        try {
            const response = await fetch(`/api/activities/?type=${this.currentFilter}&page=${this.page}`);
            const data = await response.json();
            
            if (this.page === 1) {
                this.activitiesContainer.innerHTML = '';
            }
            
            if (data.activities.length === 0 && this.page === 1) {
                this.showEmptyState();
            } else {
                this.hideEmptyState();
                this.renderActivities(data.activities);
            }
            
            this.toggleLoadMoreButton(data.has_more);
        } catch (error) {
            console.error('Error loading activities:', error);
            this.showError('Failed to load activities. Please try again.');
        } finally {
            this.isLoading = false;
            this.toggleLoading(false);
        }
    }
    
    renderActivities(activities) {
        if (activities.length === 0) return;
        
        const fragment = document.createDocumentFragment();
        
        activities.forEach(activity => {
            const activityEl = this.createActivityElement(activity);
            fragment.appendChild(activityEl);
        });
        
        if (this.page === 1) {
            this.activitiesContainer.innerHTML = '';
        }
        
        this.activitiesContainer.appendChild(fragment);
    }
    
    createActivityElement(activity) {
        const activityEl = document.createElement('div');
        activityEl.className = `activity-item relative pb-8 ${activity.is_read ? '' : 'bg-blue-50 -mx-4 px-4 py-2 rounded'}`;
        activityEl.dataset.activityId = activity.id;
        
        const iconPath = this.getIconPath(activity.type);
        const priorityClass = this.getPriorityClass(activity.priority);
        
        activityEl.innerHTML = `
            <div class="relative flex space-x-3">
                <!-- Activity icon -->
                <div>
                    <span class="h-8 w-8 rounded-full ${activity.is_important ? 'bg-red-500' : 'bg-indigo-500'} flex items-center justify-center ring-8 ring-white">
                        <svg class="h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="${iconPath}" />
                        </svg>
                    </span>
                </div>
                
                <!-- Activity content -->
                <div class="min-w-0 flex-1 pt-1 flex justify-between space-x-4">
                    <div class="flex-1">
                        <!-- Activity header -->
                        <div class="flex items-center space-x-2">
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${priorityClass}">
                                ${this.getActivityTypeLabel(activity.type)}
                            </span>
                            ${activity.is_important ? `
                            <span class="text-red-500">
                                <svg class="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
                                </svg>
                            </span>
                            ` : ''}
                        </div>
                        
                        <!-- Activity body -->
                        <p class="text-sm text-gray-500 mt-1">
                            ${this.getActivityDescription(activity)}
                        </p>
                        
                        <!-- Activity metadata -->
                        <div class="mt-1 text-xs text-gray-400">
                            <time datetime="${activity.timestamp}" title="${new Date(activity.timestamp).toLocaleString()}">
                                ${this.formatTimeAgo(activity.timestamp)}
                            </time>
                            ${activity.metadata?.source ? `
                                <span class="mx-1">•</span>
                                <span>${activity.metadata.source}</span>
                            ` : ''}
                        </div>
                    </div>
                    
                    <!-- Quick actions -->
                    <div class="flex-shrink-0 self-center opacity-0 group-hover:opacity-100 transition-opacity">
                        <div class="flex space-x-2">
                            ${this.getActionButtons(activity)}
                            <button type="button" class="mark-as-read text-gray-400 hover:text-gray-500" data-activity-id="${activity.id}">
                                <span class="sr-only">Mark as read</span>
                                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        return activityEl;
    }
    
    getIconPath(activityType) {
        const icons = {
            'course_view': 'M10 12a2 2 0 100-4 2 2 0 000 4z M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10z',
            'course_progress': 'M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0114 18.469V19a2 2 0 11-4 0v-.531c0-.895.356-1.754.988-2.386l.547-.547z',
            'resource_download': 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
            'forum_post': 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
            'forum_reply': 'M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z',
            'achievement': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
            'search': 'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
            'enroll': 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
            'complete': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
            'certificate': 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
        };
        return icons[activityType] || 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z';
    }
    
    getPriorityClass(priority) {
        return {
            'low': 'bg-blue-100 text-blue-800',
            'medium': 'bg-yellow-100 text-yellow-800',
            'high': 'bg-red-100 text-red-800',
        }[priority] || 'bg-gray-100 text-gray-800';
    }
    
    getActivityTypeLabel(type) {
        const labels = {
            'course_view': 'Course Viewed',
            'course_progress': 'Progress',
            'resource_download': 'Resource',
            'forum_post': 'Forum Post',
            'forum_reply': 'Forum Reply',
            'achievement': 'Achievement',
            'search': 'Search',
            'enroll': 'Enrollment',
            'complete': 'Completed',
            'certificate': 'Certificate',
        };
        return labels[type] || type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
    
    getActivityDescription(activity) {
        const { type, title, metadata, progress } = activity;
        
        switch (type) {
            case 'course_view':
                return `Viewed course "${title}"`;
            case 'course_progress':
                return `Made progress on "${title}"`;
            case 'search':
                return `Searched for "${metadata?.query || 'something'}"`;
            case 'enroll':
                return `Enrolled in "${title}"`;
            case 'achievement':
                return `Unlocked achievement: ${title}`;
            case 'forum_post':
                return `Posted in "${title}"`;
            case 'forum_reply':
                return `Replied in "${title}"`;
            case 'resource_download':
                return `Downloaded resource: ${title}`;
            case 'certificate':
                return `Earned certificate: ${title}`;
            default:
                return title;
        }
    }
    
    getActionButtons(activity) {
        const { type, metadata } = activity;
        
        if (['course_view', 'course_progress'].includes(type)) {
            return `
                <a href="${metadata?.course_url || '#'}" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                    Continue
                </a>
            `;
        } else if (type === 'forum_post' || type === 'forum_reply') {
            return `
                <a href="${metadata?.forum_url || '#'}" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                    View
                </a>
            `;
        } else if (type === 'certificate' && metadata?.certificate_url) {
            return `
                <a href="${metadata.certificate_url}" class="text-indigo-600 hover:text-indigo-900 text-sm font-medium">
                    View Certificate
                </a>
            `;
        }
        
        return '';
    }
    
    formatTimeAgo(timestamp) {
        const now = new Date();
        const date = new Date(timestamp);
        const seconds = Math.floor((now - date) / 1000);
        
        let interval = Math.floor(seconds / 31536000);
        if (interval >= 1) return `${interval} year${interval === 1 ? '' : 's'} ago`;
        
        interval = Math.floor(seconds / 2592000);
        if (interval >= 1) return `${interval} month${interval === 1 ? '' : 's'} ago`;
        
        interval = Math.floor(seconds / 86400);
        if (interval >= 1) return `${interval} day${interval === 1 ? '' : 's'} ago`;
        
        interval = Math.floor(seconds / 3600);
        if (interval >= 1) return `${interval} hour${interval === 1 ? '' : 's'} ago`;
        
        interval = Math.floor(seconds / 60);
        if (interval >= 1) return `${interval} minute${interval === 1 ? '' : 's'} ago`;
        
        return 'Just now';
    }
    
    async markAsRead(activityId, activityElement) {
        try {
            const response = await fetch(`/api/activities/mark-read/${activityId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                activityElement.classList.remove('bg-blue-50');
                this.updateUnreadCount();
            }
        } catch (error) {
            console.error('Error marking activity as read:', error);
        }
    }
    
    async markAllAsRead() {
        try {
            const response = await fetch('/api/activities/mark-all-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            
            if (response.ok) {
                document.querySelectorAll('.activity-item').forEach(item => {
                    item.classList.remove('bg-blue-50');
                });
                this.updateUnreadCount();
            }
        } catch (error) {
            console.error('Error marking all as read:', error);
        }
    }
    
    loadMoreActivities() {
        this.page++;
        this.loadActivities();
    }
    
    updateUnreadCount() {
        const unreadCount = document.querySelectorAll('.activity-item:not(.bg-blue-50)').length;
        const countBadge = document.getElementById('unread-count');
        
        if (countBadge) {
            if (unreadCount > 0) {
                countBadge.textContent = unreadCount;
                countBadge.classList.remove('hidden');
            } else {
                countBadge.classList.add('hidden');
            }
        }
    }
    
    toggleLoading(isLoading) {
        const loader = document.getElementById('activity-loader');
        if (loader) {
            loader.classList.toggle('hidden', !isLoading);
        }
    }
    
    showEmptyState() {
        const emptyState = document.getElementById('empty-state');
        if (emptyState) {
            emptyState.classList.remove('hidden');
        }
    }
    
    hideEmptyState() {
        const emptyState = document.getElementById('empty-state');
        if (emptyState) {
            emptyState.classList.add('hidden');
        }
    }
    
    showError(message) {
        const errorElement = document.createElement('div');
        errorElement.className = 'bg-red-50 border-l-4 border-red-400 p-4 mb-4';
        errorElement.innerHTML = `
            <div class="flex">
                <div class="flex-shrink-0">
                    <svg class="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
                    </svg>
                </div>
                <div class="ml-3">
                    <p class="text-sm text-red-700">${message}</p>
                </div>
            </div>
        `;
        
        this.activitiesContainer.prepend(errorElement);
        
        // Auto-remove error after 5 seconds
        setTimeout(() => {
            errorElement.remove();
        }, 5000);
    }
    
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

// Initialize the activity feed when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('activities-container')) {
        window.activityFeed = new ActivityFeed();
    }
});
