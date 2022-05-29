from django import forms


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_repeat = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error(None, "Password do not match!")
        if len(cleaned_data["username"]) >= 30:
            raise forms.ValidationError('Very big username!')
        if len(cleaned_data["password"]) >= 30:
            raise forms.ValidationError('Very big password!')
        if len(cleaned_data["password_repeat"]) >= 30:
            raise forms.ValidationError('Very big password_repeat!')
        return cleaned_data


class AskForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput())
    context = forms.CharField(widget=forms.Textarea())
    tags = forms.CharField(widget=forms.TextInput())

    def clean(self):
        cleaned_data = super().clean() #разбить
        if len(cleaned_data["title"]) > 30:
            raise forms.ValidationError('Very big title!')
        if len(cleaned_data["context"]) > 255:
            raise forms.ValidationError('Very big text!')
        if len(cleaned_data["tags"]) >= 30:
            raise forms.ValidationError('Very big tag!')
        return self.cleaned_data


class AnswerForm(forms.Form):
    context = forms.CharField(widget=forms.Textarea())

    def clean(self):
        cleaned_data = super().clean()
        if len(cleaned_data["context"]) > 255:
            raise forms.ValidationError('Very big text!')
