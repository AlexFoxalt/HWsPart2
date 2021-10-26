"""Here we are working with all types on Mixins that shall be imported to views.py"""

import django
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView

from users.services.services_constants import MENU
from users.services.services_error_handlers import page_not_found
from users.services.services_functions import from_dict_to_list_of_dicts_format, combine_context
from users.services.services_models import CONTEXT_CONTAINER


class EntityGeneratorMixin:
    model = None
    template_name = 'entity_generator.html'
    context_object_name = 'content'

    @classmethod
    def get(cls, request, count, user_class, *args, **kwargs):
        try:
            cls.model.generate_entity(count)
        except (IndexError, ValueError):
            return page_not_found(request, 'You should create at least 1 Course, if you want to use generator')

        posts = cls.model.objects.all().order_by('-id')[:count][::-1]

        context = {
            'title': f'{user_class} generator',
            'user_class': user_class,
            'posts': posts,
            'menu': MENU
        }
        return render(request, cls.template_name, context=context)


class EntitySearchMixinBase:
    model = None
    template_name = 'search_of_users.html'
    context_object_name = 'content'

    @classmethod
    def get_context_data(cls):
        posts = cls.model.objects.all()
        class_name = cls.model.__name__
        columns = [f.get_attname() for f in cls.model._meta.fields]

        context = {
            'title': f'{class_name}s searching',
            'user_class': f'{class_name}(s)',
            'posts': posts,
            'menu': MENU,
            'columns': columns
        }
        return context


class EntitySearchPerOneFieldMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, *args, **kwargs):
        context = super().get_context_data()
        applied_filters = []
        searching_keys = args[0]

        for key, value in searching_keys.items():
            if value is not None and value:
                context['posts'] = context['posts'].filter(**{f'{key}__contains': value})
                applied_filters.append(f'{key} --- {value}')

        context['applied_filters'] = applied_filters
        context['searching_fields'] = from_dict_to_list_of_dicts_format(searching_keys)
        return render(request, 'search_of_users.html', context=context)


class EntitySearchPerAllFieldsMixin(EntitySearchMixinBase):

    @classmethod
    def get(cls, request, text, *args, **kwargs):
        context = super().get_context_data()
        ajax_filter = request.GET.get('text', None)

        searching_keys = ajax_filter if ajax_filter is not None else text['text']

        if searching_keys is not None:
            text_fields = [f.name for f in cls.model._meta.get_fields() if
                           isinstance(f, django.db.models.fields.CharField)]
            or_cond = Q()

            for field in text_fields:
                or_cond |= Q(**{'{}__contains'.format(field): searching_keys})

            context['posts'] = context['posts'].filter(or_cond)

        context['searching_fields'] = from_dict_to_list_of_dicts_format(text)

        if request.is_ajax():
            html = render_to_string(
                template_name="posts-results-partial.html",
                context=context
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)

        return render(request, 'search_of_users.html', context=context)


class ContextMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = MENU
        context['selected'] = 0
        page_id = kwargs['page_id']

        container = CONTEXT_CONTAINER.get(page_id, None)
        context.update(container)
        return context


class GetAllUsersMixin(ContextMixin, ListView):
    def get(self, request, *args, **kwargs):
        posts = self.model.objects.all()
        columns = [f.verbose_name for f in self.model._meta.fields]
        context = self.get_user_context(page_id=self.page_id,
                                        posts=posts,
                                        columns=columns)
        return render(request, self.template_name, context=context)


class ProfileMixin(ContextMixin, DetailView):
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = self.get_user_context(page_id=self.page_id)
        return combine_context(context, extra_context)
