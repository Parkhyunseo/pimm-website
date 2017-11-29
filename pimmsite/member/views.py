from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

from .forms import LoginForm, SignupForm

def login(request):
    if request.method =='POST':
        next_path = request.GET.get('next')
        #form = LoginForm(request.POST)
        form = LoginForm(request=request, data=request.POST)
        
        if form.is_valid():
            
            user = form.get_user()
            
            
            """
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(
                username=username,
                password=password
            )
            
            # Success Loign
            if user:
                # Django의 auth앱에서 제공하는 login 함수를 실행해 앞으로의
                # 요청/응답에 세션을 유지한다.
            """
            django_login(request, user)
            #Post 목록 화면으로 이동
            #나중에는 home화면으로 변경해야함.
            return redirect(next_path if next_path else 'imagebook:post_list')
            
        form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = LoginForm()
        
    context = {
        'login_form':form,
    }
        
    return render(request, 'member/login.html', context)
        
def logout(request):
    django_logout(request)
    return redirect('imagebook:post_list')
    

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        # 유효성 검증에 통과한 경우 (username의 중복과 password1, 2의 일치 여부)
        if form.is_valid():
            # SignupForm의 인스턴스 메서드인 signup() 실행, 유저 생성
            user = form.save()
            django_login(request, user)
            return redirect('imagebook:post_list')
    else:
        form = SignupForm()

    context = {
        'signup_form': form,
    }
    return render(request, 'member/signup.html', context)