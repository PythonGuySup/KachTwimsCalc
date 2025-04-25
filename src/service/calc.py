from math import factorial

def pl_wo_rep(k: int, n: int) -> int:
    """
    Вычисляет количество размещений k элементов из n без повторений.

    Args:
        k (int): Количество размещаемых элементов.
        n (int): Общее количество элементов.

    Returns:
        int: Количество размещений.
    
    Raises:
        ValueError: Если k > n.

    Example:
        >>> pl_wo_rep(2, 5)
        20
    """
    if k > n:
        raise ValueError('Некорректные данные. Требуется: k <= n')
    return (factorial(n) / (factorial(n - k)))


def pl_w_rep(k: int, n: int) -> int:
    '''
    Вычисляет количество размещений k элементов из n с повторениями.

    Args:
        k (int): Количество размещаемых элементов.
        n (int): Общее количество элементов.

    Returns:
        int: Количество размещений.
    
    Raises:
        ValueError: Если k > n.

    Example:
        >>> pl_w_rep(2, 5)
        25
    '''
    return n ** k


def pr_w_rep(n: int,*args: int) -> float:
    '''
    Вычисляет количество перестановок k элементов из n с повторениями.

    Args:
        *args (int): Переставляемые элементы.

    Returns:
        float: Количество перестановок.
    
    Raises:
        ValueError: Если sum(k) != len(n).

    Example:
        >>> pr_w_rep(2, 2, 2)
        0.5
    '''
    
    if sum(args) != n:
        raise ValueError('Сумма аргументов не равна их количеству')
    elif n < 0:
        raise ValueError('Некорректные данные. Требуется: n >= 0')
    denominator = 1
    for arg in args:
        denominator *= factorial(arg)
    return (factorial(n) / denominator)


def pr_wo_rep(n: int) -> int:
    '''
    Вычисляет количество перестановок k элементов из n без повторений.

    Args:
        n (int): Количество переставляемых элементов.

    Returns:
        int: Количество перестановок.
    
    Raises:
        ValueError: Если k > n.

    Example:
        >>> pr_wo_rep(2)
        2
    '''
    if n < 0:
        raise ValueError('Некорректные данные. Требуется: n >= 0')
    return (factorial(n))


def cm_wo_rep(k: int, n: int) -> int:
    '''
    Вычисляет количество сочетаний k элементов из n без повторений.

    Args:
        k (int): Количество сочетаемых элементов.
        n (int): Общее количество элементов.

    Returns:
        int: Количество сочетаний.
    
    Raises:
        ValueError: Если k > 0; n > 0; k > n.

    Example:
        >>> cm_wo_rep(2, 5)
        10
    '''
    if k <= 0 and n <= 0 and k > n:
        raise ValueError('Некорректные данные. Требуется: k > 0; n > 0; k <= n')
    return (factorial(n) / (factorial(k) * factorial(n - k)))


def cm_w_rep(k: int, n: int) -> int:
    '''
    Вычисляет количество сочетаний k элементов из n с повторениями.

    Args:
        k (int): Количество сочетаемых элементов.
        n (int): Общее количество элементов.

    Returns:
        int: Количество сочетаний.
    
    Raises:
        ValueError: Если k > 0; n > 0.

    Example:
        >>> cm_w_rep(2, 5)
        15
    '''
    if k <= 0 and n <= 0:
        raise ValueError('Некорректные данные. Требуется: k > 0; n > 0')
    return cm_wo_rep(k, n + k - 1)


def all_marked(k: int, m: int, n: int) -> float:
    '''
    Вычисляет вероятность извлечения k элементов из m меченных элементов в n элементах.

    Args:
        k (int): Количество извлекаемых меченных элементов.
        m (int): Общее количество меченных элементов.
        n (int): Общее количество элементов.

    Returns:
        float: Вероятность извлечения k элементов.
    
    Raises:
        ValueError: Если k >= m или m > n.

    Example:
        >>> all_marked(2, 5, 10)
        0.22 (2)
    '''
    if k >= m or m > n:
        raise ValueError('Некорректные данные. Требуется: k < m <= n')
    return cm_wo_rep(k, m) / cm_wo_rep(k, n)


def r_marked(r: int, k: int, m: int, n: int) -> float:
    '''
    Вычисляет вероятность нахождения r меченных эелементов из k извлекаемых элементов из m меченных элементов в n элементах.

    Args:
        r (int): Количество меченных элементов.
        k (int): Количество извлекаемых элементов.
        m (int): Общее количество меченных элементов.
        n (int): Общее количество элементов.

    Returns:
        float: Вероятность нахождения r меченных элементов.
    
    Raises:
        ValueError: Если k >= m или k - r > n - m или m > n.

    Example:
        >>> r_marked(1, 2, 5, 10)
        0.55 (5)
    '''
    if k > m or k - r > n - m or m > n:
        raise ValueError('Некорректные данные. Требуется: k <= m; k - r <= n - m; m <= n')
    return (cm_wo_rep(r, m) * cm_wo_rep(k - r, n - m) / cm_wo_rep(k, n))




               