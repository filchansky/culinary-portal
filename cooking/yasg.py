from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import SwaggerAPIDoc

schema_view = get_schema_view(
    openapi.Info(
        title='Cooking API',
        default_version='v 0.0.1',
        description='API documentation for Cooking',
        terms_of_service='https://www.google.com/policies/terms',
        contact=openapi.Contact(email='example@test.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('swagger-ui/', SwaggerAPIDoc.as_view(), name='swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=1), name='schema-json'),
]
