
from django.urls import include, path
from rest_framework import routers

from faunatrack.views_api import ProjetViewset
from faunatrack.views_api import hello_world
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r'projets', ProjetViewset)

urlpatterns = [                                                                     
    path('', include(router.urls)),
    path('bonjour/', hello_world, name="hello_api"),
    # path('auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
