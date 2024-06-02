# myapp/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import  gen # Import the logout view

urlpatterns = [
    # path('register/', register, name='register'),
    # path('login/', login, name='login'),
    # path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('gen/', gen, name='gen'),
    # path('logout/', logout, name='logout'),    # Add the logout URL pattern
    # path('results/', results, name='results'), # Add the results URL pattern
]
