from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Post, Comment
from .forms import CommentForm, PostForm

from django.contrib.auth.decorators import login_required

def post_list(request):
    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    for post in posts:
        print(post.comment_set.all)
    return render(request, 'imagebook/post_list.html', context)

def post_detail(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment_form = CommentForm()
    context = {
        'post':post,
        'comment_form': comment_form,
    }
    return render(request, 'imagebook/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        # PostForm은 파일을 처리하므로 request.FILES도 함께 바인딩
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            # author필드를 채우기 위해 인스턴스만 생성
            post = post_form.save(commit=False)
            # author필드를 채운 후 DB에 저장
            post.author = request.user
            post.save()

            # 성공 알림을 messages에 추가 후 post_list뷰로 이동
            messages.success(request, '사진이 등록되었습니다')
            return redirect('imagebook:post_list')
    else:
        post_form = PostForm()

    context = {
        'post_form': post_form,
    }
    return render(request, 'imagebook/post_create.html', context)

@login_required
def comment_create(request, post_pk):
    
    # GET 파라미터로 전달된 작업 완료 후 이동할 URL 값
    next_path = request.GET.get('next')
    
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_pk)
        #content = request.POST.get('content')
        
        """
        if not content:
            print('not content')
            return HttpResponse('댓글 내용을 입력하세요.', status=400)
        """
        
        form = CommentForm(request.POST)
        
        if form.is_valid():
            # 유효성 검사에 통과하면 ModelForm의 save()호출로 인스턴스 생성
            # DB에 저장하지 않고 인스턴스만 생성하기 위해 commit=False옵션 지정 
            comment=form.save(commit=False)
            
            comment.author = request.user
            comment.post = post
            
            #DB에 저장
            comment.save()
            
            messages.success(request, '댓글이 등록되었습니다.')
        else:
            error_msg = '댓글 등록에 실패했습니다.\n{}'.format(
                '\n'.join(
                    [
                        '-{}'
                        .format(
                            error
                        )
                        for key, value in form.errors.items()
                        for error in value
                    ]
                    )
                )
            messages.error(request, error_msg)
        
        if next_path:
            return redirect(next_path)
            
        # 'imagebook' 네임스페이스를 가진 url의 'post_list'이름에 
        # 해당하는 뷰로 이동
        
        return redirect('imagebook:post_list')
     
@login_required
def post_like_toggle(request, post_pk):
    # GET 파라미터로 전달된 이동할 URL
    next_path = request.GET.get('next')
    # post_pk에 해당하는 Post객체
    post = get_object_or_404(Post, pk=post_pk)
    # 요청한 사용자
    user = request.user
    
    #사용자의 like_posts 목록에서 like_toggle할 Post가 있는지 확인
    filtered_like_posts = user.like_posts.filter(pk=post.pk)
    # 존재할 경우, like_posts 목록에서 해당 Post를 삭제 
    if filtered_like_posts.exists():
        user.like_posts.remove(post)
        
    # 없을 경우, like_posts목록에 해당 Post를 추가
    else:
        user.like_posts.add(post)
        
    # 이동할 path가 존재할 경우 해당 위치로, 없을 경우 Post상세페이지로 이동
    if next_path:
        return redirect(next_path)
        
    return redirect('imagebook:post_detail', post_pk=post_pk)
    
@login_required
def my_profile(request, user_id):
    pass
    