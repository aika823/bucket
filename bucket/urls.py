from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from user import views

urlpatterns = [
    path("", views.profile),
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("manager/", include("manager.urls")),
    path("user/", include("user.urls")),
    path("party/", include("party.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
