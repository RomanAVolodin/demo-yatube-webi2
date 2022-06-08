from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.flatpages import views

from posts import views as posts_views


handler404 = 'posts.views.page_not_found'  # noqa
handler500 = 'posts.views.server_error'  # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('django.contrib.flatpages.urls')),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('404/', posts_views.page_not_found),
    path('500/', posts_views.server_error),
]

urlpatterns += [
    path(
        'about-author/',
        views.flatpage,
        {'url': '/about-author/'},
        name='about',
    ),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name='terms'),
]

urlpatterns += [path('', include('posts.urls'))]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)