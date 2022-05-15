from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


from .models import Publisher, Review, Book

User = get_user_model()


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['cover', 'sample']

    def __init__(self, *args, **kwargs):
        super(BookMediaForm, self).__init__(*args, **kwargs)
        self.fields['cover'].widget.attrs.update({'class': 'form-control'})
        self.fields['sample'].widget.attrs.update({'class': 'form-control'})


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('creator', )
        widgets = {
            'publication_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['publication_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control'})
        self.fields['cover'].widget.attrs.update({'class': 'form-control'})
        self.fields['sample'].widget.attrs.update({'class': 'form-control'})
        self.fields['publisher'].widget.attrs.update({'class': 'form-control'})
        self.fields['contributors'].widget.attrs.update({'class': 'form-control'})


class BookDetailForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ('creator', 'cover', 'sample')
        widgets = {
            'publication_date': DateInput()
        }

    def __init__(self, *args, **kwargs):
        super(BookDetailForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['publication_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['isbn'].widget.attrs.update({'class': 'form-control'})
        self.fields['publisher'].widget.attrs.update({'class': 'form-control'})
        self.fields['contributors'].widget.attrs.update({'class': 'form-control'})


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=(
        ('title', 'Title'),
        ('contributor', 'contributor')
    ))

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['search'].widget.attrs.update({'class': 'form-control'})
        self.fields['search_in'].widget.attrs.update({'class': 'form-control'})


class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(PublisherForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['website'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=0, max_value=5)

    class Meta:
        model = Review
        exclude = ['date_edited', 'book', 'creator']

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class': 'form-control'})
        self.fields['rating'].widget.attrs.update({'class': 'form-control'})


class LoginForm(AuthenticationForm):
    pass

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].help_text = None
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})