from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/user/", include("user.urls", namespace="user")),
    path("api/", include("wine.urls", namespace="wine")),
    path("api/cart/", include("cart.urls", namespace="cart")),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/doc/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
