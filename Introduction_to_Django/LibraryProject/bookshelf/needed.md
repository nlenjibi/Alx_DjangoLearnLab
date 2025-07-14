User Registration
User registration is the process of creating new user accounts in your application. Django provides the UserCreationFormform and the CreateViewclass-based view to handle user registration.

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
In this example, the SignUpView uses the UserCreationForm to handle user registration. When a new user is registered, they are redirected to the login page using the success_url attribute.

User Login and Logout
Django’s authentication system provides built-in views and utilities for handling user login and logout processes.

User Login
from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
]
In this example, the LoginView class-based view is used to handle user login. The template_name attribute specifies the template to be rendered for the login form.

User Logout
from django.contrib.auth.views import LogoutView
from django.urls import path

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
]
The LogoutView class-based view is used to handle user logout. When a user logs out, they are redirected to the default URL specified by the LOGIN_REDIRECT_URL setting.

Customizing Authentication Views
You have the flexibility to customize these views by overriding their attributes or providing custom templates that align with your application’s design aesthetic. Additionally, you can leverage the login_required decorator or the PermissionRequiredMixin to restrict access to specific views or functionalities based on user permissions or group memberships.

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    # This view can only be accessed by authenticated users
    return render(request, 'profile.html')
Password Management
Django includes features for managing user passwords securely, such as password hashing, password validators, and password reset functionality.

Password Hashing: Django automatically hashes user passwords using the PBKDF2 algorithm before storing them in the database. This ensures that passwords are not stored in plain text, improving security.
Password Reset: Django provides built-in views and utilities for handling password reset functionality. Users can request a password reset, and Django will send them an email with a link to reset their password.
Password Validators: Django includes several built-in password validators that enforce password policies. You can use these validators or create custom ones to meet your application’s password requirements.
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
Authentication Views and URLs
Django provides several built-in views and URLs related to user authentication, including login, logout, password reset, and password change views.

Login and Logout Views
pythonCopy codefrom django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

Password Reset Views
pythonCopy codefrom django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

Password Change View
pythonCopy codefrom django.contrib.auth import views as auth_views
from django.urls import path

urlpatterns = [
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

You can customize these views by overriding their attributes or providing custom templates.

Full Example
Step 1: Enable Django Auth App
Check that the django.contrib.auth and django.contrib.contenttypes apps are in the list of installed apps, if not add them. You can do this by opening [settings.py](http://settings.py) and updating INSTALLED_APPS

INSTALLED_APPS = [
    ...
    'django.contrib.auth',
    'django.contrib.contenttypes',
    ...
]
Next make sure the following middlewares are present.

MIDDLEWARE = [
        ...,
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    ...
]
Step 2: Setting Up Urls & Redirects
Open the [urls.py](http://urls.py) file and add the required accounts urls as shown bellow

from django.urls import path, include

urlpatterns = [
    ...,

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/',
             TemplateView.as_view(template_name='accounts/profile.html'),
             name='profile'),
    path("signup/", SignUpView.as_view(), name="templates/registration/signup"),
        ...
]

Here we setup the accounts path which contains the login, logout, password change … etc routes except the signup and profile routes. These are separately added

Next, update the redirect constant variables to redirect to the profile page. Open the [settings.py](http://settings.py) file and update it as bellow

LOGIN_REDIRECT_URL = "/accounts/profile"
LOGOUT_REDIRECT_URL = "/accounts/profile"
Step 3: Adding Template Files
First create a templates folder at the root of the project and update the TEMPLATES constant in the [settings.py](http://settings.py) file as follows.

TEMPLATES = [
    {
        ...
        'DIRS': [ BASE_DIR / "templates" ],
          ...
    },
]
The following will be the expected folder structure. Assuming you have an app named myapp this can be any app including a dedicated accounts app if you like to separate account related code in to a separate app.

├── db.sqlite3
├── manage.py
├── myapp
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── mysite
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── templates
    ├── profile.html
    ├── accounts
    │   └── profile.html
    └── registration
        └── login.html
        └── signup.html
profile.html

{% if user.is_authenticated %} You are logged in as {{ user }}.
<form action="{% url 'logout' %}" method="post">
    {% csrf_token %}
    <button type="submit">Log Out</button>
</form>
{% else %} You are not logged in.
<a href="{% url 'login' %}">Click here to log in.</a>
{% endif %}
login.html

{% if form.errors %}
<p>Your username and password didn't match. Please try again.</p>
{% endif %}

<form method="post" action="{% url 'login' %}">
    {% csrf_token %} {{ form.as_p }}

    <input type="submit" value="login" />
</form>
signup.html

{% block title %}Sign Up{% endblock %} {% block content %}
<h2>Sign up</h2>
<form method="post">
    {% csrf_token %} {{ form }}
    <button type="submit">Sign Up</button>
</form>
{% endblock %}

Step 4: Adding Signup View
The next thing to do is adding a signup view. These view can be add to your existing app or to a dedicated app for handling accounts. In our case we will add this to our myapp app [views.py](http://views.py) file

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
Step 5: Migrating Your Changes and Running Your Project
The last thing to do is migrate your changes and run your project

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

