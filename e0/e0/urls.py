from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('simplechat/', include('simplechat.urls')),
    path('admin/', admin.site.urls),
]
