from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django import forms
from django.contrib.messages import add_message, SUCCESS
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, resolve_url
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse

from flatpages.models import Article, FlatPage, SupportCenterCategory, ContactUsRequest

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        kwargs['latest_articles'] = Article.objects.order_by('-created')[:3]
        return super().get_context_data(**kwargs)


class ArticleListView(ListView):
    queryset = Article.objects.all()
    context_object_name = 'articles'
    template_name = 'articles/list.html'


class ArticleDetailView(DetailView):
    queryset = Article.objects.all()
    slug_field = 'slug'
    context_object_name = 'article'
    template_name = 'articles/detail.html'


class FlatPageDetailView(DetailView):
    queryset = FlatPage.objects.all()
    slug_field = 'slug'
    context_object_name = 'flatpage'
    template_name = 'flatpages/detail.html'


class SupportCenterView(ListView):
    queryset = SupportCenterCategory.objects.prefetch_related('elements')
    context_object_name = 'categories'
    template_name = 'flatpages/support_center.html'


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsRequest
        fields = ('email', 'title', 'category', 'description')


class ContactUsView(CreateView):
    form_class = ContactUsForm
    template_name = 'flatpages/contact_us.html'

    def post(self, request, *args, **kwargs):
        # if not request.is_ajax():
        #     raise PermissionDenied

        return super().post(request, *args, **kwargs)

    def form_invalid(self, form):
        return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        form.save()
        return JsonResponse({'message': 'Contact message was sent'})


class RegisterForm(forms.ModelForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    email = forms.EmailField(label=_('Email'), required=True)
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        required=True,
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_('Repeat password'),
        strip=False,
        required=True,
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def clean(self):
        data = self.cleaned_data
        if data.get('password1') != data.get('password2'):
            self.add_error('password2', _('Password not match'))
        return data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_password(self.cleaned_data['password1'])
        if commit:
            instance.save()
        return instance


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def get_success_url(self):
        return resolve_url('login')


class SitemapView(TemplateView):
    template_name = 'sitemap.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['links'] = [
            resolve_url('flatpages:home'),
            resolve_url('flatpages:register'),
            resolve_url('login'),
            resolve_url('logout'),
            resolve_url('password_change'),
            resolve_url('password_change_done'),
            resolve_url('password_reset'),
            resolve_url('password_reset_done'),
            resolve_url('password_reset_done'),
            resolve_url('password_reset_confirm', uidb64='uidb64', token='token'),
            resolve_url('password_reset_complete'),
            resolve_url('flatpages:articles'),
            resolve_url('flatpages:article', slug='article-slug'),
            resolve_url('flatpages:contact-us'),
            resolve_url('flatpages:flatpage', slug='flatpage-slug'),
            resolve_url('flatpages:support')
        ]
        return ctx
