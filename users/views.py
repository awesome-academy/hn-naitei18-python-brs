from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordContextMixin
from django.views.generic.edit import FormView

from django.urls import reverse_lazy

from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from .forms import (
    UserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm)

from django.views.generic import (
    CreateView,
    FormView,
    TemplateView,
    ListView
)
from review.models import  Follow

from review.models import Book, BookMark, Activity

# Create your views here.

from django.http import HttpResponseRedirect


class UserDetailView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        num_following = Follow.objects.filter(follower=self.request.user).count()
        num_follower = Follow.objects.filter(following=self.request.user).count()
        read_marks = BookMark.objects.filter(user=self.request.user.id, mark_status='r_ed').order_by('-updated_at')
        reading_marks = BookMark.objects.filter(user=self.request.user.id, mark_status = 'r_ing').order_by('-updated_at')
        fa_marks = BookMark.objects.filter(user=self.request.user.id, fa_status = 'fa')
        context = super(UserDetailView, self).get_context_data(**kwargs)
        books = Book.objects.all()
        read_list = []
        reading_list = []
        fa_list = []
        for read_mark in read_marks:
            data = {'read_mark': read_mark, 'read_book': books.get(id=read_mark.book_id)}
            read_list.append(data)
        for reading_mark in reading_marks:
            data = {'reading_mark': reading_mark, 'reading_book': books.get(id=reading_mark.book_id)}
            reading_list.append(data)
        for fa_mark in fa_marks:
            data = {'fa_mark': fa_mark, 'fa_book': books.get(id=fa_mark.book_id)}
            fa_list.append(data)
        context.update({
            'following': num_following,
            'follower': num_follower,
            'read_list': read_list,
            'reading_list': reading_list,
            'fa_list': fa_list
        })
        return context

from django.http import HttpResponseRedirect
from notifications.models import Notification
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = UserUpdateForm
    p_form = ProfileUpdateForm()
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now your profile is updated!"

    def form_valid(self, form):
        self.request.user.username = self.request.POST['username']
        self.request.user.email = self.request.POST['email']
        self.request.user.save()
        return super().form_valid(form)

    def get_initial(self):
        initial = super(UserUpdateView, self).get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        return initial


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    login_url = "login"
    form_class = ProfileUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('UserProfile')
    success_message = "Now you photo is updated"

    def form_valid(self, form):
        if 'image' in self.request.FILES:
            self.request.user.profile.image = self.request.FILES['image']
            self.request.user.profile.save()
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.INFO,
                                 'Your profile pic is not change')
            return HttpResponseRedirect(reverse_lazy('UserProfile'))

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        initial['image'] = self.request.user.profile.image
        return initial

@login_required
def follow(request, pk):
    user = request.user
    to_user = get_object_or_404(User, pk=pk)
    url = request.META.get('HTTP_REFERER')
    read_marks = BookMark.objects.filter(user=to_user, mark_status='r_ed').order_by('-updated_at')
    reading_marks = BookMark.objects.filter(user=to_user, mark_status='r_ing').order_by('-updated_at')
    fa_marks = BookMark.objects.filter(user=to_user, fa_status='fa')
    books = Book.objects.all()
    read_list = []
    reading_list = []
    fa_list = []
    for read_mark in read_marks:
        data = {'read_mark': read_mark, 'read_book': books.get(id=read_mark.book_id)}
        read_list.append(data)
    for reading_mark in reading_marks:
        data = {'reading_mark': reading_mark, 'reading_book': books.get(id=reading_mark.book_id)}
        reading_list.append(data)
    for fa_mark in fa_marks:
        data = {'fa_mark': fa_mark, 'fa_book': books.get(id=fa_mark.book_id)}
        fa_list.append(data)
    if request.method == 'POST' and user != to_user:
        try:
            followed = Follow.objects.get(follower=user, following=to_user)
            followed.delete()
        except :
            follow = Follow(follower = user, following = to_user)
            follow.save()
            notify = Notification(sender=user, user=to_user, notification_type=2)
            notify.save()            
            activity = Activity(user=user, activity_type='fo', activity=follow)
            activity.save()
        return HttpResponseRedirect(url)
    else:
        if request.method == 'GET':
            user = request.user
            to_user = get_object_or_404(User, pk=pk)
            num_following = Follow.objects.filter(follower=to_user).count()
            num_follower = Follow.objects.filter(following=to_user).count()
            try:
                followed = Follow.objects.get(follower=user, following=to_user)
                is_follower =1
            except :
                is_follower=0
            context = {
                'user': user, 'to_user': to_user,
                'following': num_following,
                'follower': num_follower,
                'read_list': read_list,
                'reading_list': reading_list,
                'fa_list': fa_list,
                'is_followed': is_follower
            }
            return render(request, 'users/user_profile.html', context = context)
        else:
            return redirect('UserProfile')

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
# pip3 install six && echo import six >"$(python3 -c "import sys; print(tuple(filter(lambda x: 'site-packages' in x, sys.path))[0])")"/django/utils/__init__.py

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return render(request, 'registration/active_success.html', context={'user': user})
    else:
        return HttpResponse('Activation link is invalid!')

from django.views import generic

class UserListView(LoginRequiredMixin, generic.ListView):
    model =User
    template_name = 'users/list_users.html'
    def get_queryset(self):
        now_user = self.request.user
        # print(now_user)
        users_not_staff = User.objects.filter(is_staff = False)
        user_not_now_user = users_not_staff.exclude(id = now_user.id)
        return user_not_now_user

# class UserDetailView(LoginRequiredMixin, generic.DetailView):
#     model = User
#     template_name = 'users/user_profile.html'

class ActivityListView(ListView):
    template_name = 'users/news_feed.html'
    model = Activity

    def get_context_data(self, **kwargs):
        context = super(ActivityListView, self).get_context_data(**kwargs)
        followings = Follow.objects.filter(follower=self.request.user)
        user_list = [self.request.user]
        for following in followings:
            user_list.append(following.following)
        activity_list = Activity.objects.filter(user__in=user_list).order_by('-id')
        context.update({
            'activity_list': activity_list
        })
        return context
