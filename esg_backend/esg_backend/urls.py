

from django.contrib import admin
from django.urls import path
from api.views import get_normalized_esg_data

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', get_normalized_esg_data),
]
