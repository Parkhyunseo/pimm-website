from django import forms

from .models import Comment, Post

# ModelForm은 모델 클래스와 밀접하게 연관되어 있는 폼
# 기본적으로는 연결된 ㅗㅁ델 클래스의 필드에 해당하는 폼 요소들을 자동으로 만들어주며, 모델 클래스나
# 모델 클래스의 필드가 가진 유효성 검증도 자동으로 수행한다.

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = (
            'photo',
        )

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = (
            'content',    
        )
        widget = {
            'content': forms.TextInput(
                attrs={
                    'class': 'content',
                    'placeholder': '댓글 달기...',
                    #'size':'70px',
                    #'maxlength':'40',
                }    
            )
        }
    
    def clean_content(self):
        data = self.cleaned_data['content']
        errors = []
        if data == '':
            errors.append(forms.ValidationError('댓글 내용을 입력해주세요'))
        elif len(data) > 50:
            errors.append(forms.ValidationError('댓글 내용은 50자 이하로 입력해주세요.'))
        
        if errors:
            raise forms.ValidationError(errors)
        return data