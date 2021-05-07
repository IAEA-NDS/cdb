"""cdb URL Configuration

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
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

import cdbmeta.views

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
    [
    path(r'cdbmeta/', include('cdbmeta.urls'), name='search'),
    re_path(r'potential/(?P<potential_id>\d+)/$', cdbmeta.views.potential,
        name='potential'),
    path(r'refs/', include('refs.urls')),
    path(r'contact/',
        TemplateView.as_view(template_name='cdbmeta/contact.html'),
        name="contact"),
    path(r'licence/',
        TemplateView.as_view(template_name='cdbmeta/licence.html'),
        name="licence"),
    re_path(r'^$', cdbmeta.views.home, name='home'),
    ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# add admin urls if this functionality is enabled
if settings.ADMIN_PAGES:
	urlpatterns.extend([
		re_path(r'^admin/', admin.site.urls),
		path(r'accounts/', include('django.contrib.auth.urls'))])

if settings.UPLOAD_PAGES:
	#urlpatterns.append(path(r'cdbdata/', include('cdbdata.urls')))
	urlpatterns.append(path(r'cdbdata/', include('fallkast.urls')))
