from msilib.schema import CheckBox

from django import forms
from django.forms import RadioSelect, CheckboxInput, Select, NullBooleanSelect

from blog.models import Post, Answer
from blog.utils import DataMixinForm


class NewPostForm(DataMixinForm, forms.ModelForm):
    class Meta:
        model = Post
        fields = ['status','title','content']


class NewAnswerForm(DataMixinForm, forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']