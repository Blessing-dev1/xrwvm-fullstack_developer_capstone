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
    path(route='get_cars', view=views.get_cars, name ='getcars'),

    # path for add a review view
    # Dealerships
    path('get_dealers', views.get_dealerships, name='get_dealers'),
    path('get_dealers/<str:state>', views.get_dealerships, name='get_dealers_by_state'),

# Dealer Details
    path('dealer/<int:dealer_id>', views.get_dealer_details, name='dealer_details'),

# Dealer Reviews with Sentiment Analysis
    path('reviews/dealer/<int:dealer_id>', views.get_dealer_reviews, name='dealer_reviews'),
    path(route='add_review', view=views.add_review, name='add_review'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
