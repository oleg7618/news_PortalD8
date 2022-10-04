from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from .models import CustomUser, Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


# Подписка пользователя в категорию новостей
@login_required
def subscribe(request, pk):
    user = request.user
    subscriber = CustomUser.objects.filter(custom_user=user).last()
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)

    html_content = render_to_string(
        'subscribe_created.html',
        {
            'subscribe': subscribe,
        }
    )

    # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
    msg = EmailMultiAlternatives(
        subject=f'Подписка на {category}',
        body=category,
        to=[user],  # это то же, что и recipients_list
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html

    msg.send()  # отсылаем

    return redirect(request.META.get('HTTP_REFERER'))


class PostList(ListView):
    model = Post
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10  # постраничный вавод - указываем сколько строк будет на странице

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(
            name='authors').exists()
        return context


class PostDetail(DetailView):
    template_name = 'flatpages/post.html'
    queryset = Post.objects.all()


class PostSearch(PostList):
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filter_class = PostFilter

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    template_name = 'flatpages/add.html'
    form_class = PostForm

# дженерик для редактирования объекта


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    template_name = 'flatpages/edit.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
