from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import CustomUserChangeForm, ProfileForm, CustomUserCreationForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from pjt import settings
# 회원가입
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
            
    if request.method == 'POST':
        signup_form = CustomUserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            Profile.objects.create(user=user) # User의 Profile 생성
            auth_login(request, user)
            return redirect('movies:index')
    else:
        signup_form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'signup_form':signup_form})

# 로그인
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method =='POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        login_form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'login_form':login_form})

# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('movies:index')
    
# 내 정보
@login_required
def people(request, username):
    # get_user_model #=> User
    people = get_object_or_404(get_user_model(), username=username)
    profile = people.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'accounts/people.html', {'people':people, 'profile_form': profile_form})
    
# 회원정보 업데이트
@login_required
def update(request):
    if request.method == 'POST':
        user_change_form= CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('people', request.user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/update.html', {'user_change_form':user_change_form})
    
#회원 탈퇴   
@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('movies:index')
    return render(request, 'accounts/delete.html')
    
# 비밀번호 변경
@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            return redirect('people', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
    return render(request, 'accounts/password.html', {'password_change_form':password_change_form})

# 프로필 업데이트
@login_required
def profile_update(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('people', request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
    return render(request, 'accounts/profile_update.html', {
                                        'profile_form': profile_form,
                                    })
    
# 팔로우
def follow(request, user_id):
    people = get_object_or_404(get_user_model(), id=user_id)
    
    if request.user in people.followers.all():
        # unfollow
        people.followers.remove(request.user)
    else:
        # follow
        people.followers.add(request.user)
    
    return redirect('people', people.username)