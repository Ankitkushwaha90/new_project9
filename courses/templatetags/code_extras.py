from django import template

register = template.Library()

@register.filter
def file_extension(language):
    """Maps language names to their common file extensions"""
    extension_map = {
        'python': 'py',
        'javascript': 'js',
        'java': 'java',
        'c': 'c',
        'cpp': 'cpp',
        'csharp': 'cs',
        'go': 'go',
        'ruby': 'rb',
        'php': 'php',
        'swift': 'swift',
        'kotlin': 'kt',
        'typescript': 'ts',
        'html': 'html',
        'css': 'css',
        'sql': 'sql',
        'bash': 'sh',
        'json': 'json',
        'yaml': 'yaml',
        'markdown': 'md',
        'text': 'txt',
    }
    return extension_map.get(language, 'txt')
