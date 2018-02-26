from django import forms
from captcha.fields import CaptchaField
from users.models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空'})

    def clean(self):
        try:
            password = self.cleaned_data['password']
        except Exception as e:
            print('except: ' + str(e))
            raise forms.ValidationError(u"请输入至少6位密码")

        return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(required=True, error_messages={'required': '用户名不能为空'})
    password = forms.CharField(required=True, min_length=6, max_length=20,  error_messages={'required': '密码不能为空'})
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误", 'required': '验证码不能为空'})

    def clean(self):
        # try:
        #     password = self.cleaned_data['password']
        # except Exception as e:
        #     print('except: ' + str(e))
        #     raise forms.ValidationError(u"请输入至少6位密码")

        if UserProfile.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('用户名已经存在')

        return self.cleaned_data

