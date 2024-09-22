from django.contrib import admin
from django.urls import path, include
from datapg import views  

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('authentification/', include('authentification.urls')),  # Authentication module
    
    # View for file upload
    path('upload/', views.upload_file, name='upload_file'),
    
    # View for fetching data
    path('fetch/', views.fetch_data, name='fetch_data'),
    
    # View for calculating total hours per assistant
    path('ttl_heures/', views.ttl_heures, name='ttl_heures'),
    
    # View for calculating total hours (theoretical and real)
    path('results/', views.calculate_hours, name='calculate_hours'),
]
