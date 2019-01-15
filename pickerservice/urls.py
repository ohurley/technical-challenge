from django.conf.urls import url
from django.urls import include

from pickerservice import views
from rest_framework_swagger.views import get_swagger_view
#from rest_framework.authtoken.views import obtain_auth_token

# schema_view = get_swagger_view(title='Picker Service API')

# urlpatterns = [
    # url(r'^solve/$', views.solve_request, name='Solve'),
    # url(r'^crash/$', views.crash_request, name='Crash'),
    # url(r'^history/$', views.history_request, name='Request History'),
    # url(r'^swagger/', views.schema_view, name='Swagger UI')

    # url(r'^api-token-auth/$', obtain_auth_token, name='api_token_auth'),
# ]

my_patterns = [
    url(r'^solve/$', views.solve_request, name='Solve'),
    url(r'^crash/$', views.crash_request, name='Crash'),
    url(r'^history/$', views.history_request, name='Request History'),
    # url(r'^swagger/', views.schema_view, name='Swagger UI')
]

urlpatterns = [
    url(r'/', include(my_patterns)),
    url(r'^solve/$', views.solve_request, name='Solve'),
    url(r'^crash/$', views.crash_request, name='Crash'),
    url(r'^history/$', views.history_request, name='Request History'),
    url(r'^docs/', views.schema_view),
]

