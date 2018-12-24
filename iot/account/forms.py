from django import forms
from account.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(label='帳號', widget=forms.TextInput(attrs={'class':'input100'}))
    password = forms.CharField(label='密碼', widget=forms.PasswordInput(attrs={'class':'input100'}))
    password2 = forms.CharField(label='確認密碼', widget=forms.PasswordInput(attrs={'class':'input100'}))
    fullName = forms.CharField(label='姓名', widget=forms.TextInput(attrs={'class':'input100'}), max_length=128)
    address = forms.CharField(label='住址', widget=forms.TextInput(attrs={'class':'input100'}), max_length=128)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'fullName', 'address']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password!=password2:
            raise forms.ValidationError('密碼不相符')
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(user.password)
        if commit:
            user.save()
        return user