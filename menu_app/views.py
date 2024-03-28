from menu_app.models import Categories, Menus
from django.shortcuts import render


def catalog(request):
    context = {
        'menus': Menus.objects.all()
    }

    return render(request, 'menu_app/catalog.html', context)


def menu(request, menu_slug):
    categories_in_menu = Categories.objects.filter(menu__slug=menu_slug)
    categories = []
    for category in categories_in_menu:
        if not category.parent_category:
            categories.append({'depth': 30, 'category': category})
            print(category.menu.slug)
    context = {
        'categories': categories
    }

    return render(request, 'menu_app/index.html', context)


def category(request, category_slug):
    return render(request, 'menu_app/index.html')

    categories_in_menu = Categories.objects.filter(menu__slug=menu_slug)
    current_category = categories_in_menu.get(slug=category_slug)


    def select_parents_categories(category):
        parent_category_current_category = category.parent_category
        if parent_category_current_category is None:
            return []

        parent_category_id_current_category = parent_category_current_category.id
        last_parent_category_id = parent_category_id_current_category
        parents_categories_list = [last_parent_category_id]
        while True:
            last_parent_category_id = Categories.objects.get(id=last_parent_category_id).parent_category
            if last_parent_category_id is None:
                break

            last_parent_category_id = last_parent_category_id.id
            parents_categories_list.append(last_parent_category_id)
        return parents_categories_list




    parents_categories_list = select_parents_categories(current_category)
    parents_categories_list.append(current_category.id)
    print('список родительских категорий', parents_categories_list)
    category_and_parents_category_id = {}

    for category_from_menu in categories_in_menu:
        parent_category = category_from_menu.parent_category
        if parent_category is None:
            parent_category = None
        else:
            parent_category = parent_category.id
        category_and_parents_category_id[category_from_menu] = parent_category

        print(category_from_menu, ' - ', parent_category)

    print('category_and_len_parents_categories', category_and_parents_category_id)

    result_categories = []

    def add_category(categories, depth=1):
        print('#################\n', categories, depth)
        if len(categories) == 0:
            return
        first_in_categories = list(categories.keys())[0]
        first_in_categories_id = first_in_categories.id
        if first_in_categories_id in parents_categories_list:
            parents_categories_list.remove(first_in_categories_id)
            categories.pop(first_in_categories)
            result_categories.append({'depth': depth * 30, 'category': first_in_categories})
            sub_categories = find_keys_with_same_value(category_and_parents_category_id, first_in_categories_id)
            add_category(sub_categories, depth + 1)
            add_category(categories, depth)
        else:
            categories.pop(first_in_categories)
            result_categories.append({'depth': depth * 30, 'category': first_in_categories})
            add_category(categories, depth)

    root_categories = find_keys_with_same_value(category_and_parents_category_id, None)

    add_category(root_categories)




    context = {
        'categories': result_categories
    }
    print(context)
    # http://127.0.0.1:8000/podshipniki/sverh-zakalennye/
    return render(request, 'menu_app/index.html', context)
