from django.contrib import admin
from django.urls import path, include

from my_shop_app.api_urls import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
]
