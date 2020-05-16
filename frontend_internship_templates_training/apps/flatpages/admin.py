from django.contrib import admin

from flatpages.models import FlatPage, SupportCenterElement, SupportCenterCategory, ContactUsRequest, Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('slug', 'title')
    prepopulated_fields = {
        'slug': ('title',)
    }


@admin.register(FlatPage)
class FlatPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created', 'modified')
    readonly_fields = ('created', 'modified')
    search_fields = ('slug', 'title')
    prepopulated_fields = {
        'slug': ('title',)
    }


class SupportCenterElementInline(admin.StackedInline):
    model = SupportCenterElement
    fields = ('category', 'order', 'question', 'answer',)
    extra = 0


@admin.register(SupportCenterCategory)
class SupportCenterCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    readonly_fields = ('id',)
    prepopulated_fields = {
        'slug': ('title',)
    }
    inlines = (SupportCenterElementInline,)


@admin.register(ContactUsRequest)
class ContactUsRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'title', 'category')
