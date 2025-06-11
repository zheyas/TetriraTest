
def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        # Получим имена параметров (кроме 'return'):
        param_names = [k for k in annotations if k != 'return']
        # Проверяем только позиционные аргументы
        for name, arg in zip(param_names, args):
            if not isinstance(arg, annotations[name]):
                raise TypeError
        # Проверяем именованные аргументы
        for name, arg in kwargs.items():
            if name in annotations and not isinstance(arg, annotations[name]):
                raise TypeError
        return func(*args, **kwargs)
    return wrapper

# Тесты:
@strict
def sum_two(a: int, b: int) -> int:
    return a + b
