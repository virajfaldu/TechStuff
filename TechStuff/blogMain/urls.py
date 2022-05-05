from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls'))
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "TechStuff Admin Panel"
admin.site.site_title = "TechStuff Admin Panel"
admin.site.index_title = "Welcome To TechStuff Admin Panel"