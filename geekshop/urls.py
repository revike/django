from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from mainapp import views as mainapp

urlpatterns = [
    path('', mainapp.main, name='main'),

    path('products/', include('mainapp.urls', namespace='products')),

    path('auth/', include('authapp.urls', namespace='auth')),

    path('contacts/', mainapp.contacts, name='contacts'),

    path('basket/', include('basketapp.urls', namespace='basket')),

    # path('admin/', admin.site.urls),

    path('admin/', include('adminapp.urls', namespace='admin'))
]

handler404 = 'mainapp.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
