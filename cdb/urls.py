from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

import cdbmeta.views

urlpatterns = [
    path(r"cdbmeta/", include("cdbmeta.urls"), name="search"),
    re_path(
        r"potential/(?P<potential_id>\d+)/$", cdbmeta.views.potential, name="potential"
    ),
    path(r"refs/", include("refs.urls")),
    path(
        r"contact/",
        TemplateView.as_view(template_name="cdbmeta/contact.html"),
        name="contact",
    ),
    path(
        r"licence/",
        TemplateView.as_view(template_name="cdbmeta/licence.html"),
        name="licence",
    ),
    re_path(r"^$", cdbmeta.views.home, name="home"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        re_path(r"^__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns

# add admin urls if this functionality is enabled
if settings.ADMIN_PAGES:
    urlpatterns.extend(
        [
            re_path(r"^admin/", admin.site.urls),
            path(r"accounts/", include("django.contrib.auth.urls")),
        ]
    )

if settings.UPLOAD_PAGES:
    # urlpatterns.append(path(r'cdbdata/', include('cdbdata.urls')))
    urlpatterns.append(path(r"cdbdata/", include("fallkast.urls")))
