def fibcyt(n):
    """Fibonacci number without list"""
    a, b = 0, 1
    for item in range(3, n+1):
        a, b = b, a + b
    return b