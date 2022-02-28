from django.urls import path, include

from rest_framework.routers import DefaultRouter

from profiles_api import views

# We use DefaultRouter to register specific viewset to our register
router = DefaultRouter()
# 1st argument: the name of URL we want to create 'hello-viewset'
# 2nd argument: name of viewset
# 3rd argument: base_name
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')

# No need to specify basename, because in UserProfileViewSet we have queryset
# Django will figure out the name from model that assign to it.
# We only specify basename if:
# No queryset
# We want to override the name of queryset associate to it.
router.register('profile-viewset', views.UserProfileViewSet);

# Register feed
router.register('feed', views.ProfileFeedViewSet)

urlpatterns = [
    # Register ApiView to urls
    path('hello-view/', views.HelloApiView.as_view()),
    # Register login view
    path('login/', views.UserLoginApiView.as_view()),
    # Register ViewSet to urls
    path('', include(router.urls))  # blank string is we don't want any prefix to urls
]
