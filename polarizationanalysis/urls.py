from django.conf.urls import url
from polarizationanalysis import views

# Specific URL settings.
urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    url(r'^processInput$',views.CustomersPageView.processInput),
]
