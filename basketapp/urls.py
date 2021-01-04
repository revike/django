from django.urls import path
import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.add, name='add'),
    # path('delete/<int:pk>/', basketapp.delete, name='delete'),
    path('delete/ajax/<int:pk>/<int:quantity>/', basketapp.delete_ajax, name='delete_ajax'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.edit, name='edit'),
]
