"""
Setup configuration for Django API Project
"""
from setuptools import setup, find_packages

# Read requirements from requirements.txt
def read_requirements(filename):
    """Read requirements from a file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f 
                if line.strip() and not line.startswith('#')]

setup(
    name="django-api-project",
    version="1.0.0",
    description="A comprehensive Django REST API project",
    long_description=open("README.md").read() if open("README.md") else "",
    long_description_content_type="text/markdown",
    author="ALX Django Learn Lab",
    author_email="your-email@example.com",
    url="https://github.com/nlenjibi/Alx_DjangoLearnLab",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.11",
    install_requires=[
        # Core Django and API Framework
        "django>=5.1.0,<5.2.0",
        "djangorestframework>=3.15.0,<3.16.0",
        
        # Authentication
        "djangorestframework-simplejwt>=5.3.0,<5.4.0",
        
        # API Enhancement
        "django-filter>=24.0,<25.0",
        "markdown>=3.7.0,<4.0.0",
        
        # Image handling
        "Pillow>=11.0.0,<12.0.0",
        
        # HTTP requests
        "requests>=2.32.0,<3.0.0",
        
        # Database
        "psycopg2-binary>=2.9.0,<3.0.0",
        
        # Environment management
        "python-decouple>=3.8.0,<4.0.0",
        
        # CORS handling
        "django-cors-headers>=4.6.0,<5.0.0",
        
        # API documentation
        "drf-spectacular>=0.28.0,<1.0.0",
        
        # Caching
        "redis>=5.2.0,<6.0.0",
        "django-redis>=5.4.0,<6.0.0",
    ],
    extras_require={
        "dev": [
            # Development and Debugging
            "django-debug-toolbar>=4.4.0,<5.0.0",
            
            # Testing
            "pytest>=8.3.0,<9.0.0",
            "pytest-django>=4.9.0,<5.0.0",
            "factory-boy>=3.3.0,<4.0.0",
            "coverage>=7.6.0,<8.0.0",
            "pytest-cov>=6.0.0,<7.0.0",
            
            # Code quality
            "black>=24.10.0,<25.0.0",
            "flake8>=7.1.0,<8.0.0",
            "isort>=5.13.0,<6.0.0",
            "pre-commit>=3.8.0,<4.0.0",
            
            # Documentation
            "sphinx>=8.1.0,<9.0.0",
            "sphinx-rtd-theme>=3.0.0,<4.0.0",
        ],
        "production": [
            # Production-specific packages
            "gunicorn>=23.0.0,<24.0.0",
            "whitenoise>=6.8.0,<7.0.0",
            "django-extensions>=3.2.0,<4.0.0",
        ],
        "monitoring": [
            # Monitoring and logging
            "sentry-sdk>=2.19.0,<3.0.0",
            "django-prometheus>=2.3.0,<3.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "django-api=manage:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
