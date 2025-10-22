def add(a: int, b: int) -> int:
    """Soma dois números e retorna o resultado."""
    return a + b


def divide(a: int, b: int) -> float:
    """Divide a por b, tratando divisão por zero."""
    if b == 0:
        raise ValueError("Divisão por zero não permitida")
    return a / b


if __name__ == "__main__":
    print("Exemplo Trustable: soma =", add(3, 5))
    print("Exemplo Trustable: divisão =", divide(10, 2))
