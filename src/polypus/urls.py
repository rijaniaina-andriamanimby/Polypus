from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from client.urls import index_client
from publication.urls import acceuil_publication

# path('admin/', admin.site.urls)
urlpatterns = [
    path('admin/', index_client, name="pageAcceuil"),
    path('employer/', include('employer.urls')),
    path('reservation/', include('reservation.urls')),
    path('Model-villa/', include('villa.urls')),
    path('Ville/', include('ville.urls')),
    path('residence/', include('resider.urls')),
    path('villa/', include('villaUnique.urls')),
    path('client/', include('client.urls')),
    path('publication/', include('publication.urls')),
    path('', acceuil_publication, name="acceuilPublication"),
    path('accounts/', include('accounts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
