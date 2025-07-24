"""
Django Security Testing Script
This script performs basic security checks on the Django application.
"""

import os
import django
from django.core.management import execute_from_command_line
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

User = get_user_model()

class SecurityTester:
    def __init__(self):
        self.client = Client()
        self.test_results = []
    
    def log_result(self, test_name, passed, message=""):
        """Log test results"""
        status = "PASS" if passed else "FAIL"
        self.test_results.append(f"[{status}] {test_name}: {message}")
        print(f"[{status}] {test_name}: {message}")
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        print("\n=== Testing CSRF Protection ===")
        
        # Test POST without CSRF token
        response = self.client.post('/bookshelf/', {'title': 'Test Book'})
        self.log_result(
            "CSRF Protection", 
            response.status_code == 403 or 'csrfmiddlewaretoken' in str(response.content),
            "Forms properly protected with CSRF tokens"
        )
    
    def test_xss_prevention(self):
        """Test XSS prevention in input fields"""
        print("\n=== Testing XSS Prevention ===")
        
        # Create a test user with appropriate permissions
        try:
            user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
            self.client.login(username='testuser', password='testpass123')
            
            # Test XSS in search
            xss_payload = '<script>alert("XSS")</script>'
            response = self.client.get('/bookshelf/', {'search': xss_payload})
            
            # Check if script tags are escaped
            escaped = '&lt;script&gt;' in response.content.decode() or '<script>' not in response.content.decode()
            self.log_result(
                "XSS Prevention",
                escaped,
                "Script tags properly escaped in output"
            )
            
        except Exception as e:
            self.log_result("XSS Prevention", False, f"Error: {e}")
    
    def test_sql_injection_prevention(self):
        """Test SQL injection prevention"""
        print("\n=== Testing SQL Injection Prevention ===")
        
        try:
            # Test SQL injection in search
            sql_payload = "'; DROP TABLE bookshelf_book; --"
            response = self.client.get('/bookshelf/', {'search': sql_payload})
            
            # If we get a response without error, ORM handled it safely
            self.log_result(
                "SQL Injection Prevention",
                response.status_code in [200, 302, 403],
                "ORM safely handles malicious SQL in search"
            )
            
        except Exception as e:
            self.log_result("SQL Injection Prevention", False, f"Error: {e}")
    
    def test_permission_enforcement(self):
        """Test that permissions are properly enforced"""
        print("\n=== Testing Permission Enforcement ===")
        
        try:
            # Test access without authentication
            response = self.client.get('/bookshelf/')
            self.log_result(
                "Unauthenticated Access",
                response.status_code in [302, 403],  # Redirect to login or forbidden
                "Unauthenticated users properly redirected"
            )
            
            # Test access with authenticated user but no permissions
            user = User.objects.create_user('noperms', 'noperms@example.com', 'testpass123')
            self.client.login(username='noperms', password='testpass123')
            
            response = self.client.get('/bookshelf/')
            self.log_result(
                "Permission Enforcement",
                response.status_code == 403,
                "Users without permissions properly denied access"
            )
            
        except Exception as e:
            self.log_result("Permission Enforcement", False, f"Error: {e}")
    
    def test_input_validation(self):
        """Test input validation"""
        print("\n=== Testing Input Validation ===")
        
        try:
            # Test extremely long input
            long_input = "A" * 1000
            response = self.client.get('/bookshelf/', {'search': long_input})
            
            # Should handle gracefully (redirect or show error)
            self.log_result(
                "Input Length Validation",
                response.status_code in [200, 302],
                "Long inputs handled gracefully"
            )
            
        except Exception as e:
            self.log_result("Input Validation", False, f"Error: {e}")
    
    def test_security_headers(self):
        """Test security headers in responses"""
        print("\n=== Testing Security Headers ===")
        
        try:
            response = self.client.get('/bookshelf/')
            headers = response.headers
            
            # Check for key security headers
            security_checks = [
                ('X-Content-Type-Options', 'nosniff'),
                ('X-Frame-Options', 'DENY'),
                ('X-XSS-Protection', '1; mode=block'),
            ]
            
            for header, expected_value in security_checks:
                if header in headers and expected_value in headers[header]:
                    self.log_result(f"Security Header {header}", True, f"Present with value: {headers[header]}")
                else:
                    self.log_result(f"Security Header {header}", False, "Missing or incorrect value")
                    
        except Exception as e:
            self.log_result("Security Headers", False, f"Error: {e}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("=" * 60)
        print("DJANGO SECURITY TEST SUITE")
        print("=" * 60)
        
        self.test_csrf_protection()
        self.test_xss_prevention()
        self.test_sql_injection_prevention()
        self.test_permission_enforcement()
        self.test_input_validation()
        self.test_security_headers()
        
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        for result in self.test_results:
            print(result)
        
        passed = len([r for r in self.test_results if '[PASS]' in r])
        total = len(self.test_results)
        
        print(f"\nResults: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All security tests passed!")
        else:
            print("⚠️  Some security tests failed. Please review the implementation.")
        
        return passed == total

if __name__ == "__main__":
    tester = SecurityTester()
    success = tester.run_all_tests()
    
    if not success:
        exit(1)
