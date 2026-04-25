"""Модуль analysis/urls.py.

Містить функціональність застосунку Avelon Healthcare."""
from __future__ import annotations
from django.urls import path
from analysis.views import add_to_cart_view, analysis_list_view, cart_detail_view, head_manager_analysis_create_view, head_manager_analysis_list_view, head_manager_analysis_update_view, remove_from_cart_view
app_name = 'analysis'
urlpatterns = [path('', analysis_list_view, name='analysis_list'), path('cart/', cart_detail_view, name='cart_detail'), path('add/<int:analysis_id>/', add_to_cart_view, name='add_to_cart'), path('remove/<int:analysis_id>/', remove_from_cart_view, name='remove_from_cart'), path('head-manager/analysis/', head_manager_analysis_list_view, name='head_manager_analysis_list'), path('head-manager/analysis/create/', head_manager_analysis_create_view, name='head_manager_analysis_create'), path('head-manager/analysis/<int:pk>/update/', head_manager_analysis_update_view, name='head_manager_analysis_update')]
