# HTTPS Deployment Configuration Guide

## Overview

This guide provides comprehensive instructions for deploying your Django application with HTTPS support, ensuring secure communication between clients and your server.

## Table of Contents

1. [Django HTTPS Configuration](#django-https-configuration)
2. [SSL/TLS Certificate Setup](#ssltls-certificate-setup)
3. [Web Server Configuration](#web-server-configuration)
4. [Environment Variables](#environment-variables)
5. [Testing HTTPS Implementation](#testing-https-implementation)
6. [Troubleshooting](#troubleshooting)

---

## Django HTTPS Configuration

### Settings Overview

Your Django application has been configured with the following HTTPS security settings:

```python
# Environment-based HTTPS activation
USE_HTTPS = os.environ.get('USE_HTTPS', 'False').lower() == 'true'

# HTTPS Redirect Settings
SECURE_SSL_REDIRECT = True  # Redirects all HTTP to HTTPS
SECURE_REDIRECT_EXEMPT = []  # No exempt URLs for maximum security

# HTTP Strict Transport Security (HSTS)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure Cookies
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# Proxy Support
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
```

### Security Benefits

- **SECURE_SSL_REDIRECT**: Automatically redirects HTTP requests to HTTPS
- **HSTS**: Prevents downgrade attacks and cookie hijacking
- **Secure Cookies**: Ensures cookies are only transmitted over encrypted connections
- **Proxy Support**: Works with reverse proxies and load balancers

---

## SSL/TLS Certificate Setup

### Option 1: Let's Encrypt (Free SSL Certificate)

#### Prerequisites

- Domain name pointing to your server
- Root access to your server
- Certbot installed

#### Installation Steps

1. **Install Certbot** (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain SSL Certificate**:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Auto-renewal Setup**:

```bash
sudo crontab -e
# Add this line for auto-renewal
0 12 * * * /usr/bin/certbot renew --quiet
```

### Option 2: Commercial SSL Certificate

1. **Generate Certificate Signing Request (CSR)**:

```bash
openssl req -new -newkey rsa:2048 -nodes -keyout yourdomain.key -out yourdomain.csr
```

2. **Purchase and Download Certificate** from your SSL provider

3. **Install Certificate** on your web server

### Option 3: Self-Signed Certificate (Development Only)

```bash
# Generate private key
openssl genpkey -algorithm RSA -out private.key -pkcs8

# Generate self-signed certificate
openssl req -new -x509 -key private.key -out certificate.crt -days 365
```

---

## Web Server Configuration

### Nginx Configuration

Create `/etc/nginx/sites-available/libraryproject`:

```nginx
# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server block
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /path/to/your/certificate.crt;
    ssl_certificate_key /path/to/your/private.key;

    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Django application
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/your/project/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Media files
    location /media/ {
        alias /path/to/your/project/media/;
    }
}
```

### Apache Configuration

Create `/etc/apache2/sites-available/libraryproject-ssl.conf`:

```apache
# HTTP to HTTPS redirect
<VirtualHost *:80>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

# HTTPS Virtual Host
<VirtualHost *:443>
    ServerName yourdomain.com
    ServerAlias www.yourdomain.com

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /path/to/your/certificate.crt
    SSLCertificateKeyFile /path/to/your/private.key
    SSLCertificateChainFile /path/to/your/chain.crt

    # Modern SSL configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off

    # Security headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options "DENY"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"

    # Django application
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    ProxyPreserveHost On
    ProxyAddHeaders On
</VirtualHost>
```

---

## Environment Variables

### Production Environment Setup

Create a `.env` file or set environment variables:

```bash
# Enable HTTPS security
export USE_HTTPS=true

# Production settings
export DEBUG=false
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database settings (example)
export DATABASE_URL=postgresql://user:password@localhost/dbname

# Secret key (generate a new one for production)
export SECRET_KEY=your-production-secret-key
```

### systemd Service File

Create `/etc/systemd/system/libraryproject.service`:

```ini
[Unit]
Description=Library Project Django Application
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=libraryproject
WorkingDirectory=/path/to/your/project
Environment=USE_HTTPS=true
Environment=DEBUG=false
Environment=ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ExecStart=/path/to/your/venv/bin/gunicorn LibraryProject.wsgi:application \
          --bind 127.0.0.1:8000 \
          --workers 3 \
          --timeout 120
ExecReload=/bin/kill -s HUP $MAINPID
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

---

## Testing HTTPS Implementation

### 1. Local Testing with Development Server

```bash
# Set environment variable for HTTPS testing
export USE_HTTPS=true

# Start Django development server
python manage.py runserver
```

### 2. SSL Configuration Tests

#### Test SSL Certificate:

```bash
# Check certificate details
openssl s_client -connect yourdomain.com:443 -servername yourdomain.com

# Test certificate expiration
openssl s_client -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

#### Test HTTPS Redirect:

```bash
# Should return 301 redirect
curl -I http://yourdomain.com

# Should return 200 OK
curl -I https://yourdomain.com
```

### 3. Security Headers Verification

```bash
# Check security headers
curl -I https://yourdomain.com

# Expected headers:
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
```

### 4. Online SSL Testing Tools

- **SSL Labs**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **Mozilla Observatory**: https://observatory.mozilla.org/

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Mixed Content Warnings

**Problem**: Resources loaded over HTTP on HTTPS page
**Solution**: Update all resource URLs to use HTTPS or relative URLs

#### 2. CSRF Token Mismatch

**Problem**: CSRF verification fails after enabling HTTPS
**Solution**: Clear browser cookies and ensure `CSRF_COOKIE_SECURE` matches your environment

#### 3. Session Loss

**Problem**: Users get logged out frequently
**Solution**: Check `SESSION_COOKIE_SECURE` setting and cookie domain configuration

#### 4. Proxy/Load Balancer Issues

**Problem**: Redirect loops or HTTPS not detected
**Solution**: Configure `SECURE_PROXY_SSL_HEADER` correctly

```python
# For AWS ALB/ELB
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# For Cloudflare
SECURE_PROXY_SSL_HEADER = ('HTTP_CF_VISITOR', '"scheme":"https"')
```

### Debug Commands

```bash
# Check Django security settings
python manage.py check --deploy

# Test SSL configuration
python manage.py shell
>>> from django.conf import settings
>>> print(f"SSL Redirect: {settings.SECURE_SSL_REDIRECT}")
>>> print(f"HSTS Seconds: {settings.SECURE_HSTS_SECONDS}")
>>> print(f"Cookie Secure: {settings.SESSION_COOKIE_SECURE}")
```

### Log Monitoring

Monitor your logs for HTTPS-related issues:

```bash
# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# Django security logs
tail -f /path/to/your/project/security.log

# System logs
journalctl -u libraryproject -f
```

---

## Security Checklist

- [ ] SSL certificate installed and valid
- [ ] HTTP to HTTPS redirect working
- [ ] HSTS headers present
- [ ] Secure cookies enabled
- [ ] Security headers configured
- [ ] Mixed content issues resolved
- [ ] SSL Labs grade A or A+
- [ ] Auto-renewal setup for certificates
- [ ] Monitoring and alerting configured
- [ ] Backup and recovery procedures tested

---

## Conclusion

This deployment configuration ensures your Django application meets modern security standards for HTTPS implementation. Regular monitoring and updates are essential to maintain security over time.

For additional security considerations, refer to:

- `SECURITY_IMPLEMENTATION_GUIDE.md`
- `PERMISSIONS_SETUP_GUIDE.md`
- Django's security documentation: https://docs.djangoproject.com/en/stable/topics/security/
