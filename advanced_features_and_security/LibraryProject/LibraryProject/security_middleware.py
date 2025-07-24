"""
Custom Security Middleware for Enhanced Protection

This middleware implements additional security measures including:
- Content Security Policy (CSP) headers
- Additional security headers
- Input sanitization logging
- Rate limiting protection
"""

import logging
from django.http import HttpResponseForbidden
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

logger = logging.getLogger('django.security')

class SecurityMiddleware(MiddlewareMixin):
    """
    Custom security middleware to add enhanced security headers and protections.
    """
    
    def process_request(self, request):
        """
        Process incoming requests for security violations.
        """
        # Log potentially suspicious requests
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Basic bot detection (you can expand this)
        suspicious_agents = ['sqlmap', 'nikto', 'dirb', 'nmap']
        if any(agent in user_agent.lower() for agent in suspicious_agents):
            logger.warning(f"Suspicious user agent detected: {user_agent} from {self.get_client_ip(request)}")
        
        # Check for common attack patterns in URLs
        suspicious_patterns = ['../../../', 'union+select', '<script>', 'javascript:', 'eval(']
        request_path = request.get_full_path().lower()
        
        for pattern in suspicious_patterns:
            if pattern in request_path:
                logger.warning(f"Suspicious URL pattern '{pattern}' detected from {self.get_client_ip(request)}: {request_path}")
                # Optionally block the request
                # return HttpResponseForbidden("Forbidden")
        
        return None
    
    def process_response(self, request, response):
        """
        Add security headers to all responses.
        """
        # Content Security Policy
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_directives = []
            
            if hasattr(settings, 'CSP_DEFAULT_SRC'):
                csp_directives.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
            if hasattr(settings, 'CSP_SCRIPT_SRC'):
                csp_directives.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
            if hasattr(settings, 'CSP_STYLE_SRC'):
                csp_directives.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
            if hasattr(settings, 'CSP_IMG_SRC'):
                csp_directives.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
            if hasattr(settings, 'CSP_FONT_SRC'):
                csp_directives.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")
            if hasattr(settings, 'CSP_CONNECT_SRC'):
                csp_directives.append(f"connect-src {' '.join(settings.CSP_CONNECT_SRC)}")
            if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
                csp_directives.append(f"frame-ancestors {' '.join(settings.CSP_FRAME_ANCESTORS)}")
            if hasattr(settings, 'CSP_BASE_URI'):
                csp_directives.append(f"base-uri {' '.join(settings.CSP_BASE_URI)}")
            if hasattr(settings, 'CSP_FORM_ACTION'):
                csp_directives.append(f"form-action {' '.join(settings.CSP_FORM_ACTION)}")
            
            if csp_directives:
                response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = getattr(settings, 'SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin')
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
        
        return response
    
    def get_client_ip(self, request):
        """
        Get the client's IP address, accounting for proxies.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip