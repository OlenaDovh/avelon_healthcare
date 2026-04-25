"""Модуль avelon_healthcare/urls.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
urlpatterns = [path('admin/', admin.site.urls), path('', include('core.urls')), path('accounts/', include('accounts.urls')), path('doctors/', include('doctors.urls')), path('appointments/', include('appointments.urls')), path('analysis/', include('analysis.urls')), path('orders/', include('orders.urls')), path('reviews/', include('reviews.urls')), path('support-chat/', include('support_chat.urls'))]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
