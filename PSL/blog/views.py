from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.forms import NewPostForm, NewAnswerForm
from blog.models import Post, Answer

from .utils import *


class BlogView(ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog/main.html'
    context_object_name = 'posts'
    ordering = '-time_create'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог разработки проекта'
        context['menu'] = menu
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = NewPostForm
    template_name = 'blog/new_post.html'
    success_url = reverse_lazy('blog')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Новое сообщение'
        context['menu'] = menu
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class DetailPostView(DetailView):
    model = Post
    template_name = 'blog/detail_post.html'
    context_object_name = 'post'
    ordering = 'time_create'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сообщение'
        context['menu'] = menu
        context['pk_url_kwarg'] = 'pk'
        return context


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = NewPostForm
    # fields = ['title', 'content']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование'
        context['menu'] = menu
        return context


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление'
        context['menu'] = menu
        return context


# class CreateAnswerView(CreateView):
#     model = Answer
#     form_class = NewAnswerForm
#     template_name = 'blog/new_answer.html'
#     success_url = reverse_lazy('blog')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Новый комментарий'
#         context['post'] = self.post
#         return context
#
#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         # form.instance.post = self.kwargs.get("post_id")
#         form.save()
#         return super().form_valid(form)

def new_answer(request, pk):
    error = ''
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        answer = Answer()
        answer.post = post
        answer.author = request.user
        form = NewAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('blog')
        else:
            error = "Форма заполнена не верно"
    form = NewAnswerForm()
    context = {
        'menu': menu,
        'form': form,
        'error': error,
        'post': post,
        'author': request.user,
    }
    return render(request, 'blog/new_answer.html', context)


def admin_view(request):
    return redirect('admin')