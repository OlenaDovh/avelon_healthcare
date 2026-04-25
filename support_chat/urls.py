"""Модуль support_chat/urls.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.urls import path
from . import views

app_name = 'support_chat'
urlpatterns = [path('current-session/', views.get_current_chat_session_view, name='current_session'),
               path('create-session/', views.create_chat_session_view, name='create_session'),
               path('session/<int:session_id>/', views.get_chat_session_view, name='get_session'),
               path('operator/dashboard/', views.operator_dashboard_view, name='operator_dashboard'),
               path('operator/dashboard-data/', views.operator_dashboard_data_view, name='operator_dashboard_data'),
               path('operator/claim/<int:session_id>/', views.claim_chat_view, name='claim_chat'),
               path('operator/room/<int:session_id>/', views.operator_chat_room_view, name='operator_chat_room')]
