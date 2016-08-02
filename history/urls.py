from django.conf.urls import url, include
from themes.oregon.history import views

urlpatterns = [
  url(r'^/$', views.history, name="oregon_history"),
  url(r'^/(?P<essay>\w+)$', views.essay, name="oregon_history_essay"),
]
