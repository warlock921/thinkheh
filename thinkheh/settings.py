"""
Django settings for thinkheh project.

Generated by 'django-admin startproject' using Django 1.11.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
# from django.core.urlresolvers import reverse_lazy 

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#注意、特别注意，此key千万不能修改，否则报错，无法启动服务器！！！！
#备份：SECRET_KEY = '#s!(q#1&-k7v5ic0o%8i^q2=nlzv&eu%9dhe@*v26+v_jj2bbx'
SECRET_KEY = '#s!(q#1&-k7v5ic0o%8i^q2=nlzv&eu%9dhe@*v26+v_jj2bbx'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost","192.168.20.24","0.0.0.0","10.0.0.16"]


# Application definition

INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mainsite',
    'account',
    'article',
    'actions',
    'imageload',
    'sorl.thumbnail',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'thinkheh.urls'

LOGIN_REDIRECT_URL = '/mainsite/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'thinkheh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thinkheh',
        'USER': 'root',
        'PASSWORD': 'P@ssword',
        "HOST": "192.168.10.201",

    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_FORMAT = 'Y-m-d H:i:s'  # suit在admin里设置时间的一个小bug。需要把时间格式指定一下
DATE_FORMAT = 'Y-m-d'

SUIT_CONFIG = {
    'ADMIN_NAME': '红企家园-后台管理',  #登录界面提示
    'HEADER_DATE_FORMAT': 'Y-m-d',
    'HEADER_TIME_FORMAT': 'H:i',
    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'LIST_PER_PAGE': 20,
    'MENU_OPEN_FIRST_CHILD': True,
    # 'MENU': (
    #     {'app': 'auth', 'label': u'权限管理', 'icon': 'icon-lock'},
    #     '-',
    #     {'app': 'duser', 'label': u'平台用户', 'icon': 'icon-user'},
    #     '-',
    #     {'app': 'dtheme', 'label': u'主题管理', 'icon': 'icon-tags'},
    #     '-',
    #     {'app': 'dpost', 'label': u'文章管理', 'icon': 'icon-edit'},
    #     '-'
    #     )
}



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,"static")
]
STATICFILES_FINDERS = (  
    'django.contrib.staticfiles.finders.FileSystemFinder',  
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',  
)  

#发送的验证邮件配置
EMAIL_HOST = 'smtp.qq.com'
EMAIL_HOST_USER = "840246464@qq.com"
EMAIL_HOST_PASSWORD = "vudbntmpjlnnbdbg"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "840246464@qq.com"

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
MEDIA_URL = '/static/image_upload/'
MEDIA_ROOT = os.path.join(BASE_DIR,"static/image_upload/").replace('\\','/')

#Redis设置,这里是必须的，请勿修改参数,host参数地址指向的是数据库服务器（可按需修改）
REDIS_HOST = '192.168.10.201'    #按需修改，localhost 或 数据库所在服务器IP地址
REDIS_PORT = 6379   #端口号请勿修改
REDIS_DB = 0        #DB参数请勿修改

# #生成规范的URL
# ABSOLUTE_URL_OVERRIDES = {
#     'auth.user': lambda u: reverse_lazy('user_detail',args=[u.username])
# }
