from django.contrib import admin
from django.urls import path, include
from users.views import LoginView, LogoutView, CookieTokenRefreshView
from projects.views import ProjectListView, ProjectCreateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("projects/", ProjectListView.as_view(), name="projects"),
    path("projects/create/", ProjectCreateView.as_view(), name="create_project"),
]
