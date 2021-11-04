from django.contrib import admin
from django.urls import path, include, re_path
from user import views

urlpatterns = [
    path('', views.profile ),
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    # path('api/', include('rest_framework.urls')),
    # path('api/', include('rest_framework.urls')),
    # path('api/product/', ProductListAPI.as_view()),
    # path('api/product/<int:pk>/', ProductDetailAPI.as_view()),
]
