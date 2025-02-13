from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls', namespace='account')),
    path('index/', include('ticket.urls')),  # Этот маршрут должен идти последним
]
