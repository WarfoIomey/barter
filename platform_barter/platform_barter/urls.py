from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls.static import static
from django.conf import settings


handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.failure_server'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls', namespace='ads')),
    path('api/', include('api.urls', namespace='api')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('ads:index'),
        ),
        name='registration',
    ),
    path('pages/', include('pages.urls', namespace='pages')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
