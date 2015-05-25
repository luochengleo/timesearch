from django.conf.urls import patterns, include, url
from django.contrib import admin

from anno.views import hello
from anno.views import current_datetime
from anno.views import train
from anno.views import search
from anno.views import validate
from anno.views import login
from anno.views import log
from anno.views import tasks
from anno.views import annolist
from anno.views import annotation
from anno.views import log_annotation
from anno.views import log_session_annotation
from anno.views import log_questionnaire
from anno.views import questionnaire
from anno.views import log_query_satisfaction
from anno.views import description
from anno.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timesearch.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^admin/', include(admin.site.urls)),
    (r'^hello/$',hello),
    (r'^search/(\d{1,2})/(.*?)/(\d{1,2})/$',search),
    (r'^train/(\d{1,2})/$',train),
    (r'^validate/(\d{1,2})/$',validate),
    (r'^login/$',login),
    (r'^tasks/(\d{10})/(.*?)/$',tasks),
    (r'^annolist/(\d{1,2})/$',annolist),
    (r'^annotation/(\d{1,2})/(.*?)/$', annotation),
    (r'^taskreview/(\d{1,2})/$', taskreview),
    (r'^questionnaire/(\d{1,2})/$', questionnaire),
    (r'^description/(\d{1,2})/(.*?)/$', description),
    (r'^LogService/$', log),
    (r'^AnnoService/$', log_annotation),
    (r'^SessionAnnoService/$', log_session_annotation),
    (r'^QuestionnaireService/$', log_questionnaire),
    (r'^QuerySatisfactionService/$', log_query_satisfaction)
)
