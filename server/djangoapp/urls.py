# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import logout_view
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    path('login', view=views.login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
