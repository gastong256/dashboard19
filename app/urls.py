from django.urls import path
from app.views import index, signup

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup, name="signup"),
]  