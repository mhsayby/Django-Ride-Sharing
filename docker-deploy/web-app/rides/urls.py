from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,

    PostDeleteView,
    UserPostListView,

    PendingPostListView,
    FilteredPendingPostListView,
    PendingStatusUpdateView,
    PendingJoinUpdateView,
    ConfirmedPostListView,
    FindPendingPostListView,
    ConfirmedStatusUpdateView,
    CompletedPostListView,
)
from . import views
from users import views as user_views

urlpatterns = [
    path('', views.home, name='rides-home'),

    path('post/<str:username>/pending', PendingPostListView.as_view(), name='pending-posts'),
    path('post/<str:username>/filtered_pending', FilteredPendingPostListView.as_view(), name='filtered-pending-posts'),
    path('post/<str:username>/confirmed', ConfirmedPostListView.as_view(), name='confirmed-posts'),
    path('post/<str:username>/find_pending', FindPendingPostListView.as_view(), name='find-pending-posts'),
    path('post/<str:username>/completed', CompletedPostListView.as_view(), name='completed-posts'),

    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),

    path('post/<int:pk>/pending_status/', PendingStatusUpdateView.as_view(), name='pending-post-status-update'),
    path('post/<int:pk>/confirmed_join/', PendingJoinUpdateView.as_view(), name='pending-post-join'),
    path('post/<int:pk>/confirmed_status/', ConfirmedStatusUpdateView.as_view(), name='confirmed-post-status-update'),

    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='rides-about'),
]
