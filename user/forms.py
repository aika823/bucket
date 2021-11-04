from django import forms
from .models import User
from django.contrib.auth.hashers import check_password


class LoginForm(forms.Form):
    username = forms.CharField(
        label="사용자 이름",
        max_length=32, 
        error_messages={'required': '아이디를 입력해주세요.'}
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput, 
        error_messages={'required': '비밀번호를 입력해주세요.'}
    )
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        image = cleaned_data.get('image')
        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.add_error('username', '아이디가 없습니다')
                return
            if not check_password(password, user.password):
                self.add_error('password', 'password: {} user.passwor: {}'.format(password, user.password))
            else:
                self.user_id = user.id

class RegisterForm(forms.Form):
    username = forms.CharField(
        error_messages={'required': '유저명을 입력해주세요.'},
        max_length=64, 
        label='유저명'
    )
    email = forms.CharField(
        error_messages={'required': '이메일'},
        max_length=128, 
        label='이메일'
    )
    password = forms.CharField(
        label="비밀번호",
        widget=forms.PasswordInput, 
        error_messages={'required': '비밀번호를 입력해주세요.'}
    )
    re_password = forms.CharField(
        label="비밀번호 확인",
        widget=forms.PasswordInput, 
        error_messages={'required': '비밀번호를 입력해주세요.'}
    )
    # image = forms.ImageField(
    #     error_messages={'required': '이미지를 입력해주세요.'}, 
    #     label='이미지',
    # )
    image = forms.FileField(
        error_messages={'required': '이미지를 입력해주세요.'}, 
        label='이미지!',
        widget=forms.FileInput(attrs={'accept':'image/*,video/*'})
    ) 