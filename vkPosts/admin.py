from django.contrib import admin

# Register your models here.
from django import forms
from .models import Post


class AddPostForm (forms.ModelForm):

    post_text = forms.CharField(max_length=1000)
    post_name = forms.CharField(max_length=100)
    post_url = forms.CharField(max_length=300)

    def save(self, commit=True):
        p = super(AddPostForm, self).save(commit=False)
        p.name = self.cleaned_data['post_name']
        p.directlink = self.cleaned_data['post_url']
        p.setAllAttributes(self.cleaned_data['post_text'])
        if commit:
            p.save()
        return p

    class Meta:
        model = Post
        fields = ['post_text', 'post_name', 'post_url']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class PostAdmin(admin.ModelAdmin):
    form = AddPostForm
    #add_form = AddPostForm

    # fieldsets = (
    #     (None, {
    #         'fields': ('name', 'direct_link', 'element_id', 'owner_id', 'post_id', 'post_hash',)
    #     }),
    # )
    # add_fieldsets = (
    #     (None, {
    #         'fields': ('post_text',)
    #     }),
    # )


admin.site.register(Post, PostAdmin)
