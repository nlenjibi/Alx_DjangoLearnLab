#!/usr/bin/env python
"""
HTTPS Security Testing Script
This script tests the HTTPS implementation and security configuration.
"""

import os
import sys
import requests
import urllib3
from urllib.parse import urlparse
import ssl
import socket
from datetime import datetime

# Disable SSL warnings for testing
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class HTTPSSecurityTester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.https_url = base_url.replace('http://', 'https://')
        self.results = []
        
    def test_https_redirect(self):
        """Test if HTTP requests are redirected to HTTPS"""
        print("🔄 Testing HTTPS redirect...")
        
        try:
            response = requests.get(self.base_url, allow_redirects=False, timeout=10)
            
            if response.status_code in [301, 302, 307, 308]:
                location = response.headers.get('Location', '')
                if location.startswith('https://'):
                    print("✅ HTTPS redirect: WORKING")
                    self.results.append(("HTTPS Redirect", "PASS", "HTTP correctly redirects to HTTPS"))
                    return True
                else:
                    print("❌ HTTPS redirect: FAILED - Redirects but not to HTTPS")
                    self.results.append(("HTTPS Redirect", "FAIL", f"Redirects to: {location}"))
            else:
                print("⚠️  HTTPS redirect: NOT CONFIGURED - HTTP requests not redirected")
                self.results.append(("HTTPS Redirect", "WARN", f"HTTP returns {response.status_code}"))
                
        except requests.exceptions.RequestException as e:
            print(f"❌ HTTPS redirect test failed: {e}")
            self.results.append(("HTTPS Redirect", "ERROR", str(e)))
            
        return False
    
    def test_security_headers(self):
        """Test for presence of security headers"""
        print("🔄 Testing security headers...")
        
        try:
            response = requests.get(self.https_url, verify=False, timeout=10)
            headers = response.headers
            
            # Expected security headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS protection',
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME-sniffing protection',
                'X-XSS-Protection': 'XSS filtering',
                'Referrer-Policy': 'Referrer information control'
            }
            
            for header, description in security_headers.items():
                if header in headers:
                    print(f"✅ {header}: {headers[header]}")
                    self.results.append((header, "PASS", headers[header]))
                else:
                    print(f"❌ {header}: MISSING")
                    self.results.append((header, "FAIL", "Header not present"))
                    
        except requests.exceptions.RequestException as e:
            print(f"❌ Security headers test failed: {e}")
            self.results.append(("Security Headers", "ERROR", str(e)))
    
    def test_cookie_security(self):
        """Test cookie security attributes"""
        print("🔄 Testing cookie security...")
        
        try:
            response = requests.get(self.https_url + '/admin/', verify=False, timeout=10)
            
            # Check Set-Cookie headers for security attributes
            set_cookies = response.headers.get_list('Set-Cookie') if hasattr(response.headers, 'get_list') else []
            
            if not set_cookies:
                # Try to get cookies from a form page
                response = requests.get(self.https_url + '/bookshelf/', verify=False, timeout=10)
                set_cookies = response.headers.get_list('Set-Cookie') if hasattr(response.headers, 'get_list') else []
            
            secure_cookies = []
            httponly_cookies = []
            samesite_cookies = []
            
            for cookie in set_cookies:
                if 'Secure' in cookie:
                    secure_cookies.append(cookie.split(';')[0])
                if 'HttpOnly' in cookie:
                    httponly_cookies.append(cookie.split(';')[0])
                if 'SameSite' in cookie:
                    samesite_cookies.append(cookie.split(';')[0])
            
            if secure_cookies:
                print(f"✅ Secure cookies: {len(secure_cookies)} found")
                self.results.append(("Secure Cookies", "PASS", f"{len(secure_cookies)} cookies with Secure flag"))
            else:
                print("⚠️  Secure cookies: None found (may require login)")
                self.results.append(("Secure Cookies", "WARN", "No cookies with Secure flag found"))
                
            if httponly_cookies:
                print(f"✅ HttpOnly cookies: {len(httponly_cookies)} found")
                self.results.append(("HttpOnly Cookies", "PASS", f"{len(httponly_cookies)} cookies with HttpOnly flag"))
            else:
                print("⚠️  HttpOnly cookies: None found")
                self.results.append(("HttpOnly Cookies", "WARN", "No cookies with HttpOnly flag found"))
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Cookie security test failed: {e}")
            self.results.append(("Cookie Security", "ERROR", str(e)))
    
    def test_ssl_certificate(self):
        """Test SSL certificate configuration (for HTTPS URLs)"""
        print("🔄 Testing SSL certificate...")
        
        if not self.https_url.startswith('https://'):
            print("⚠️  SSL certificate: Skipping (not HTTPS URL)")
            return
            
        try:
            parsed_url = urlparse(self.https_url)
            hostname = parsed_url.hostname
            port = parsed_url.port or 443
            
            # Create SSL context
            context = ssl.create_default_context()
            
            # Connect and get certificate
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate validity
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    if days_until_expiry > 30:
                        print(f"✅ SSL Certificate: Valid for {days_until_expiry} more days")
                        self.results.append(("SSL Certificate", "PASS", f"Valid for {days_until_expiry} days"))
                    elif days_until_expiry > 0:
                        print(f"⚠️  SSL Certificate: Expires in {days_until_expiry} days")
                        self.results.append(("SSL Certificate", "WARN", f"Expires in {days_until_expiry} days"))
                    else:
                        print("❌ SSL Certificate: EXPIRED")
                        self.results.append(("SSL Certificate", "FAIL", "Certificate expired"))
                        
        except Exception as e:
            print(f"❌ SSL certificate test failed: {e}")
            self.results.append(("SSL Certificate", "ERROR", str(e)))
    
    def test_django_security_settings(self):
        """Test Django security configuration"""
        print("🔄 Testing Django security settings...")
        
        # This would require access to Django settings
        # We'll check based on response behavior instead
        
        try:
            # Test CSRF protection
            response = requests.post(self.https_url + '/bookshelf/', 
                                   data={'test': 'data'}, 
                                   verify=False, 
                                   timeout=10)
            
            if response.status_code == 403:
                print("✅ CSRF Protection: Active (403 Forbidden for POST without token)")
                self.results.append(("CSRF Protection", "PASS", "POST requests properly protected"))
            else:
                print(f"⚠️  CSRF Protection: Status {response.status_code} (may need authentication)")
                self.results.append(("CSRF Protection", "WARN", f"Unexpected status: {response.status_code}"))
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Django security test failed: {e}")
            self.results.append(("Django Security", "ERROR", str(e)))
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🛡️  HTTPS Security Testing")
        print("=" * 50)
        
        # Run individual tests
        self.test_https_redirect()
        print()
        self.test_security_headers()
        print()
        self.test_cookie_security()
        print()
        self.test_ssl_certificate()
        print()
        self.test_django_security_settings()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 50)
        print("📊 SECURITY TEST SUMMARY")
        print("=" * 50)
        
        pass_count = sum(1 for _, status, _ in self.results if status == "PASS")
        warn_count = sum(1 for _, status, _ in self.results if status == "WARN")
        fail_count = sum(1 for _, status, _ in self.results if status == "FAIL")
        error_count = sum(1 for _, status, _ in self.results if status == "ERROR")
        
        total_tests = len(self.results)
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {pass_count}")
        print(f"⚠️  Warnings: {warn_count}")
        print(f"❌ Failed: {fail_count}")
        print(f"🔥 Errors: {error_count}")
        
        # Calculate security score
        security_score = (pass_count * 100) // max(total_tests, 1) if total_tests > 0 else 0
        
        print(f"\n🎯 Security Score: {security_score}%")
        
        if security_score >= 90:
            print("🏆 Excellent security configuration!")
        elif security_score >= 75:
            print("👍 Good security configuration with minor issues")
        elif security_score >= 50:
            print("⚠️  Adequate security but needs improvement")
        else:
            print("🚨 Security configuration needs significant attention")
        
        # Detailed results
        print("\n📋 Detailed Results:")
        print("-" * 50)
        for test_name, status, details in self.results:
            status_icon = {
                "PASS": "✅",
                "WARN": "⚠️ ",
                "FAIL": "❌",
                "ERROR": "🔥"
            }.get(status, "❓")
            
            print(f"{status_icon} {test_name}: {details}")
        
        # Recommendations
        print("\n💡 Recommendations:")
        print("-" * 50)
        
        if fail_count > 0 or error_count > 0:
            print("• Fix failing tests before deploying to production")
        if warn_count > 0:
            print("• Review warnings and consider improvements")
        
        print("• Enable HTTPS in production with USE_HTTPS=true")
        print("• Use a trusted SSL certificate from a recognized CA")
        print("• Regularly test security configuration")
        print("• Monitor SSL certificate expiration")
        print("• Keep Django and dependencies updated")

def main():
    """Main function"""
    # Check if URL provided as argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    print(f"Testing URL: {base_url}")
    print(f"HTTPS URL: {base_url.replace('http://', 'https://')}")
    print()
    
    # Create tester and run tests
    tester = HTTPSSecurityTester(base_url)
    tester.run_all_tests()
    
    print(f"\n🎯 Run this script again after deploying with HTTPS enabled!")
    print("   Example: python test_https_security.py https://yourdomain.com")

if __name__ == "__main__":
    main()
