from django.urls import path
from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns
from todo import views
#from . import views

urlpatterns = [
    
    url(r'^desks/$', views.desk_list),
    url(r'^todo/(?P<pk>\w+)/$', views.company_todo),

    url(r'^desks/detail/$', views.desk_detail),

    url(r'^users/', views.UserList.as_view()),
    url(r'^auth/(?P<pk>\w+)/$', views.auth_user),
    url(r'^users/(?P<pk>\d+)/$', views.UserDetail.as_view()),
    url(r'^registration/', views.create_auth),
]

urlpatterns = format_suffix_patterns(urlpatterns)

