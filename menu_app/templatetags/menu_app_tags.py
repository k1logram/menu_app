from django.urls import resolve
from django.utils.http import urlencode
from django import template
from menu_app.models import Categories, Menus
from django.utils.safestring import mark_safe
from django.template import Template, Context



register = template.Library()


def find_keys_with_same_value(dictionary, target_value):
    result = {}

    for category in list(dictionary.keys()):
        if dictionary[category] == target_value:
            result[category] = dictionary[category]

    return result


def select_parents_categories(category_slug, menu_slug, categories_in_menu, categories_parents_dict):
    if category_slug != menu_slug:
        for category in categories_in_menu:
            if category.slug == category_slug:
                current_category = category
        parents_categories_list = select_parents_categories_for_category(current_category.id, categories_parents_dict, categories_in_menu)

    else:
        parents_categories_list = []

    return parents_categories_list


def select_parents_categories_for_category(category_id, categories_parents_dict, categories_in_menu, parents_categories=None):
    if parents_categories is None:
        parents_categories = []

    parents_categories.append(category_id)
    parent_category_current_category = categories_parents_dict[category_id]
    if parent_category_current_category is None:
        return parents_categories

    else:
        return select_parents_categories_for_category(parent_category_current_category, categories_parents_dict, categories_in_menu, parents_categories)


def create_menu_html(result_categories):
    menu_html = ''
    link_template = Template(
        '<a class="category-dropdown-header__all-products" href="{% url "menu_app:category" category_slug %}">{{ category_name }}</a>')

    for item in result_categories:
        context = Context({
            'category_slug': item["category"].slug,
            'category_name': item["category"].name
        })
        menu_html += f'<p><button class="category-dropdown-header__button" type="button" tabindex="-1" style="opacity: 0.8; margin-left: {item["depth"]}px;">'
        menu_html += link_template.render(context)
        menu_html += '</button></p>'

    return menu_html


def get_category_slug_from_context(context):
    request = context['request']
    current_url = request.get_full_path()
    resolved_url = resolve(current_url)
    category_slug = resolved_url.kwargs.get('category_slug', None)
    return category_slug

def get_categories_parents_dict(categories_in_menu):
    categories_parents_dict = {}
    for category in categories_in_menu:
        if category.parent_category is None:
            parent_id = None
        else:
            parent_id = category.parent_category.id

        categories_parents_dict[category.id] = parent_id

    return categories_parents_dict


def get_categories_objects_parents_dict(categories_in_menu):
    categories_parents_dict = {}
    for category in categories_in_menu:
        if category.parent_category is None:
            parent_id = None
        else:
            parent_id = category.parent_category.id

        categories_parents_dict[category] = parent_id

    return categories_parents_dict


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_slug):
    # Находим slug категории которую нужно отобразить
    category_slug = get_category_slug_from_context(context)

    categories_in_menu = Categories.objects.filter(menu__slug=menu_slug).select_related('parent_category')
    # Собираем словарь всех родительских категорий {id категории: id родительской категории}
    categories_parents_dict = get_categories_parents_dict(categories_in_menu)

    # Собираем список id категорий которые нужно отобразить развернутые, в том числе id текущей
    parents_categories_list = select_parents_categories(category_slug, menu_slug, categories_in_menu, categories_parents_dict)

    # Собираем словарь всех родительских категорий {объект категории: id родительской категории}
    category_and_parents_category_id = get_categories_objects_parents_dict(categories_in_menu)

    # Берем словарь {объект категории: id родительской категории} для категорий у которых нет родительской
    root_categories = find_keys_with_same_value(category_and_parents_category_id, None)

    result_categories = []

    def get_categories_scheme_from_menu(categories, depth=1):
        if len(categories) == 0:
            return
        first_category = list(categories.keys())[0]
        first_category_id = first_category.id
        categories.pop(first_category)

        # Если id категории есть в списке всех родительских категорий текущей из url и её собственного id
        if first_category_id in parents_categories_list:
            parents_categories_list.remove(first_category_id)
            result_categories.append({'depth': depth * 30, 'category': first_category})
            # Берем все дочерние категории, и запускаем для них с увеличением глубины (отступ от края страницы)
            sub_categories = find_keys_with_same_value(category_and_parents_category_id, first_category_id)
            get_categories_scheme_from_menu(sub_categories, depth + 1)
            get_categories_scheme_from_menu(categories, depth)

        else:
            result_categories.append({'depth': depth * 30, 'category': first_category})
            get_categories_scheme_from_menu(categories, depth)

    # Генерируем список словарей [{глубина, категория}] в порядке по которому они будут в меню
    get_categories_scheme_from_menu(root_categories)

    menu_html = create_menu_html(result_categories)
    return mark_safe(menu_html)
