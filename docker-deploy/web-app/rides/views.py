from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
import os
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post


def home(request):
    context = {
        'posts': Post.objects.all(),
    }
    return render(request, 'rides/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'rides/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'rides/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PendingPostListView(ListView):
    model = Post
    template_name = 'rides/pending_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.profile.status == "driver":
            return Post.objects.filter(status='pending').exclude(author=user).exclude(sharer=user.username).order_by('-date_posted')
        elif user.profile.status == "owner":
            return Post.objects.filter(status='pending').filter(author=user).exclude(sharer=user.username).order_by('-date_posted')
        elif user.profile.status == "sharer":
            return Post.objects.filter(status='pending').filter(sharer=user.username).exclude(author=user).order_by('-date_posted')


class FilteredPendingPostListView(ListView):
    model = Post
    template_name = 'rides/pending_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.profile.status == "driver":
            filtered_posts = Post.objects.filter(status='pending')
            if Post.type != "":
                filtered_posts = filtered_posts.filter(type=user.profile.type)
            if Post.volume != "":
                filtered_posts = filtered_posts.filter(volume__lte=str(user.profile.volume))
            return filtered_posts.exclude(author=user).exclude(sharer=user.username).order_by('-date_posted')
        elif user.profile.status == "sharer":
            filtered_posts = Post.objects.filter(status='pending')
            if user.profile.search_dest != "":
                filtered_posts = filtered_posts.filter(destination=user.profile.search_dest)
            if user.profile.search_time != "":
                filtered_posts = filtered_posts.filter(arrival_time=user.profile.search_time)
            if user.profile.search_type != "":
                filtered_posts = filtered_posts.filter(type=user.profile.search_type)
            if user.profile.search_volume != "":
                filtered_posts = filtered_posts.filter(volume=user.profile.search_volume)
            return filtered_posts.exclude(author=user).exclude(sharer=user.username).order_by('-date_posted')


class FindPendingPostListView(ListView):
    model = Post
    template_name = 'rides/pending_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.profile.status == "sharer":
            return Post.objects.filter(status='pending').filter(sharer="None").exclude(author=user).exclude(driver=user.username).order_by('-date_posted')


class ConfirmedPostListView(ListView):
    model = Post
    template_name = 'rides/confirmed_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.profile.status == "driver":
            return Post.objects.filter(status='confirmed').filter(driver=user.username).order_by('-date_posted')
        elif user.profile.status == "owner":
            return Post.objects.filter(status='confirmed').filter(author=user).order_by('-date_posted')
        elif user.profile.status == "sharer":
            return Post.objects.filter(status='confirmed').filter(sharer=user.username).order_by('-date_posted')


class CompletedPostListView(ListView):
    model = Post
    template_name = 'rides/completed_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user.profile.status == "driver":
            return Post.objects.filter(status='completed').filter(driver=user.username).order_by('-date_posted')
        elif user.profile.status == "owner":
            return Post.objects.filter(status='completed').filter(author=user).order_by('-date_posted')
        elif user.profile.status == "sharer":
            return Post.objects.filter(status='completed').filter(sharer=user.username).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','destination','arrival_time','type','volume','special']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','destination','arrival_time','type','volume','special']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PendingStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = []

    def send_email_to_owner_and_sharer(self, form):
        owner = get_object_or_404(User, username=form.instance.author)
        receivers = [owner.email]
        if (form.instance.sharer != "None"):
            sharer = get_object_or_404(User, username=form.instance.sharer)
            receivers.append(sharer.email)
        send_mail(
            'Ride Confirmed Notification from Ride-Sharing',
            'Your ride has been confirmed. Thanks for using our app.',
            "ridesharing95@gmail.com",
            receivers,
            fail_silently = False)

    def form_valid(self, form):
        form.instance.status = "confirmed"
        form.instance.driver = self.request.user.username
        form.instance.type = self.request.user.profile.type
        form.instance.plate = self.request.user.profile.plate
        form.instance.volume = self.request.user.profile.volume
        self.send_email_to_owner_and_sharer(form)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile.status == "driver":
            return True
        return False


class PendingJoinUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = []

    def form_valid(self, form):
        form.instance.sharer = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile.status == "sharer":
            return True
        return False


class ConfirmedStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    fields = []

    def form_valid(self, form):
        if self.request.user.profile.status == "driver":
            form.instance.status = "completed"
            form.instance.driver = self.request.user.username
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user.profile.status in ["driver"]:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'rides/about.html', {'title': 'About'})