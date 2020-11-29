from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),
    
    path('products/', include('mainapp.urls', namespace='mainapp')),

    path('contacts/', mainapp.contacts, name='contacts'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
