from django.urls import path
from expenses.api.views import (
    UserListCreateView, 
    UserDetailView, 
    ExpenseListCreateView, 
    ExpenseDetailView, 
    ExpenseDateRangeView,
    ExpenseCategorySummaryView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger configuration
schema_view = get_schema_view(
   openapi.Info(
      title="Expense Tracker API",
      default_version='v1',
      description="API for tracking expenses",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Swagger documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('users/', UserListCreateView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),


    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
   
    path('users/<int:user_id>/expenses/date-range/', 
         ExpenseDateRangeView.as_view(), 
         name='expense-date-range'),
    path('users/<int:user_id>/expenses/category-summary/<int:year>/<int:month>/', 
         ExpenseCategorySummaryView.as_view(), 
         name='expense-category-summary'),
    

]