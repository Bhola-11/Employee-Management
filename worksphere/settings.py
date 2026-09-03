import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-worksphere-enterprise-hrms-production-super-secret-key'

DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # WorkSphere Core Apps
    'apps.core.apps.CoreConfig',
    'apps.accounts.apps.AccountsConfig',
    'apps.organizations.apps.OrganizationsConfig',
    'apps.employees.apps.EmployeesConfig',
    'apps.recruitment.apps.RecruitmentConfig',
    'apps.onboarding.apps.OnboardingConfig',
    'apps.attendance.apps.AttendanceConfig',
    'apps.shifts.apps.ShiftsConfig',
    'apps.leave_management.apps.LeaveManagementConfig',
    'apps.holidays.apps.HolidaysConfig',
    'apps.compensation.apps.CompensationConfig',
    'apps.payroll.apps.PayrollConfig',
    'apps.benefits.apps.BenefitsConfig',
    'apps.expenses.apps.ExpensesConfig',
    'apps.travel.apps.TravelConfig',
    'apps.performance.apps.PerformanceConfig',
    'apps.learning.apps.LearningConfig',
    'apps.assets.apps.AssetsConfig',
    'apps.documents.apps.DocumentsConfig',
    'apps.helpdesk.apps.HelpdeskConfig',
    'apps.analytics.apps.AnalyticsConfig',
    'apps.notifications.apps.NotificationsConfig',
    'apps.audit.apps.AuditConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.TenantMiddleware',
    'apps.core.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'worksphere.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.worksphere_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'worksphere.wsgi.application'
ASGI_APPLICATION = 'worksphere.asgi.application'

# Database - SQLite as required for local MVP
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 6},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

# Celery Configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_ALWAYS_EAGER = True  # Allows local sync execution without mandatory running redis during local dev

# WorkSphere HRMS Global Settings
WORKSPHERE_APP_NAME = 'WorkSphere'
WORKSPHERE_TAGLINE = 'One Platform for Every Workforce'
WORKSPHERE_VERSION = '1.0.0-Enterprise'
