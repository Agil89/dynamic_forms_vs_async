from django.urls import path
from mForms.views import FormsView,FormCreateView

app_name = 'forms'

urlpatterns = [
    path('forms/<int:pk>',FormsView.as_view(),name='form-fields'),
    path('submit/',FormCreateView.as_view(), name='form-submit'),
    # path('emails/',EmailCreateView.as_view(),name='email-list'),
]