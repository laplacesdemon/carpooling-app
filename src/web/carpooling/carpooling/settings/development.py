"""
Development settings for carpooling project.
"""
from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS += (
    'django_extensions',
    #'debug_toolbar',
    #'debug_toolbar_user_panel',
    'django_nose',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

WSGI_APPLICATION = 'carpooling.wsgi.development.application'

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    #'zula_cms.middleware.apiactivitylogger.ApiActivityLoggerMiddleware',
)

###################################
# Debug Toolbar Settings          #
###################################

DEBUG_TOOLBAR_PANELS = [
    #'debug_toolbar_user_panel.panels.UserPanel',
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    #'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    #'EXTRA_SIGNALS': ['myproject.signals.MySignal'],
    #'HIDE_DJANGO_SQL': False,
    #'TAG': 'div',
    #'ENABLE_STACKTRACES' : True,
}

###################################
# Testing Settings
###################################

use_nose = True

if not use_nose:
    TEST_RUNNER = 'django_test_coverage.runner.CoverageTestSuiteRunner'
    #COVERAGE_MODULES = ('zoo.baer', 'zoo.lion')
    COVERAGE_EXCLUDE_MODULES = ()
    #COVERAGE_APPS = ('zoo',)
    COVERAGE_REPORT_TYPE = 'html'
    COVERAGE_HTML_DIRECTORY = '../covhtml/'
else:
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        '-s',  # don't capture debugger statements
        #'--pdb',
        #'--pdb-failures',
        '--with-noseexclude',
        '--exclude-dir=migrations',
        '--with-cov',
        '--cov-report=html',
        '--cov=ride',
        #'--failed',
        #'--logging-filter=zula_core,zula_htmlfive',
        '--logging-level=INFO',
        #'--with-progressive',
    ]
