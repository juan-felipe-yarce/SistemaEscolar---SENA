from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # 👈 Esto hace que las rutas de core estén en la raíz
    path('logout/', LogoutView.as_view(next_page='inicio'), name='logout'),  # <-- Aquí el logout real
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += [
#        path('__debug__/', include(debug_toolbar.urls)),
#     ]
