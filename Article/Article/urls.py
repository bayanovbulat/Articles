"""Article URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

from Article import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'login/', views.LoginView.as_view(), name = "login"),
	url(r'logout/', views.LogoutView.as_view(), name = "logout"),
	url(r'registration/', views.registration, name = "registration"),
	url(r'registrationeditors/', views.registration_editors, name = "registrationeditors"),
	url(r'^$', views.ArticleListView.as_view(), name = 'articles'),
	url(r'^releases$', views.ReleaseListView.as_view(), name = 'releases'),
	url(r'^edit/(?P<id>\d+)$', views.article_update, name = 'edit'),
	url(r'^update/(?P<index>\d+)$', views.article_edit, name = 'articleeditor'),
	url(r'^add/$', views.article_create, name = 'add'),
	url(r'^articleadd/(?P<id>\d+)$', views.article_add, name = 'articleadd'),
	url(r'^addrelease/$', views.release_create, name = 'addrelease'),
	url(r'^delete/(?P<id>\d+)$', views.article_delete, name = "delete"),
	url(r'^article/(?P<id>\d+)$', views.article, name = 'article'),
	url(r'^article/(?P<index>\d+)/(?P<id>\d+)$', views.articlerelease, name = 'articlerelease'),
	url(r'^release/(?P<index>\d+)$', views.release, name = 'release'),
	url(r'^upload/$', views.upload_file, name = 'upload'),
]
