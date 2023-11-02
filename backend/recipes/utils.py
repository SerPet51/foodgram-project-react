from rest_framework import exceptions


def double_checker(item_list):
    """Проверяет элементы на повтор"""
    for item in item_list:
        if len(item) == 0:
            raise exceptions.ValidationError(
                f'{item} должен иметь хотя бы одну позицию!'
            )
        for element in item:
            if item.count(element) > 1:
                raise exceptions.ValidationError(
                    f'{element} уже есть в рецепте!'
                )
