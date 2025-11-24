from sympy import symbols, parse_expr, E, lambdify
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
    convert_xor,
)


class IntervaloInvalido(Exception):
    pass


def escolha_metodo():
    while True:
        print(
            "\nEscolha a formula desejada:\n",
            "1) Newton-Cotes Fechada\n",
            "2) Newton-Cotes Aberta\n",
        )
        escolha = input("Digite o número (1 ou 2): ").strip()
        if escolha == "1":
            return "F"
        elif escolha == "2":
            return "A"
        else:
            print("\nErro: Entrada inválida. Por favor, digite apenas 1 ou 2.\n")


def tabela_ou_funcao():
    while True:
        print(
            "\nEscolha o tipo do input:\n",
            "1) Função\n",
            "2) Tabela\n",
        )
        escolha = input("Digite o número (1 ou 2): ").strip()
        if escolha == "1":
            return "F"
        elif escolha == "2":
            return "T"
        else:
            print("\nErro: Entrada inválida. Por favor, digite apenas 1 ou 2.\n")


def regra_trapezio(x0, x1, f):
    h = x1 - x0
    soma = f(x0) + f(x1)
    return h / 2 * soma


def regra_simpson(x0, x2, f):
    h = (x2 - x0) / 2
    x1 = x0 + h
    soma = f(x0) + 4 * f(x1) + f(x2)

    return h / 3 * soma


def regra_simpson_3_8(x0, x3, f):
    h = (x3 - x0) / 3
    soma = f(x0) + f(x3)

    for i in range(1, 3):
        xi = x0 + i * h
        soma += 3 * f(xi)

    return 3 * h / 8 * soma


def regra_boole(x0, x4, f):
    h = (x4 - x0) / 4
    x1 = x0 + h
    x2 = x0 + 2 * h
    x3 = x0 + 3 * h
    soma = 7 * f(x0) + 32 * f(x1) + 12 * f(x2) + 32 * f(x3) + 7 * f(x4)
    return (2 * h / 45) * soma


def newton_cotes_fechadas(a, b, f, n):
    if n == 1:
        return regra_trapezio(a, b, f)
    elif n == 2:
        return regra_simpson(a, b, f)
    elif n == 3:
        return regra_simpson_3_8(a, b, f)
    elif n == 4:
        return regra_boole(a, b, f)
    return None


def regra_ponto_medio(a, b, f):
    h = b - a / 2
    x0 = a + h
    return 2 * h * f(x0)


def abertas_um(a, b, f):
    h = b - a / 3
    x0 = a + h
    x1 = b - h
    soma = f(x0) + f(x1)
    return 3 * h / 2 * soma


def regra_milne(a, b, f):
    h = b - a / 4
    x0 = a + h
    x1 = x0 + h
    x2 = b - h

    soma = 2 * f(x0) - f(x1) + 2 * f(x2)
    return 4 * h / 3 * soma


def abertas_tres(a, b, f):
    h = a - b / 5
    x0 = a + h
    x1 = x0 + h
    x2 = x0 + h * 2
    x3 = b - h

    soma = 11 * f(x0) + f(x1) + f(x2) + 11 * f(x3)
    return 5 * h / 24 * soma


def newton_cotes_abertas(a, b, f, n):
    if n == 0:
        return regra_ponto_medio(a, b, f)
    elif n == 1:
        return abertas_um(a, b, f)
    elif n == 2:
        return regra_milne(a, b, f)
    elif n == 3:
        return abertas_tres(a, b, f)
    return None


def ler_tabela(n):
    print(f"Insira os valores da tablea com {n} pontos")

    pontos = []
    h = 0

    for i in range(n):
        if i >= 2:
            h = abs(pontos[i - 1] - pontos[i - 2])
        numero = input(f"Insira o ponto {i}: ").strip()
        if abs(pontos[i] - pontos[i - 1] != h):
            raise IntervaloInvalido
        pontos.append(numero)

    return pontos


def ler_funcao():
    x = symbols("x", real=True)  # Define x como variável real
    f = input("Insira a função f(x): ").strip()
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )  # Permite que o parse aceite '^' = **, 'ax' = a * x, e^a = exp(a)
    locals_vars = {
        "x": x,
        "e": E,
    }  # Permite que o parse reconhece e = exp() e x como variável
    f = parse_expr(
        f, local_dict=locals_vars, transformations=transformations
    )  # Converte o input numa expressão sympy
    f = lambdify(x, f, modules="math")  # Converte a função em método

    return f


def escolha_pontos(tipo):
    while True:
        n = int(input("Insira o número de pontos: "))
        if (tipo == "F" and (n < 1 or n > 4)) or (tipo == "A" and (n < 0 or n > 3)):
            print("Pontos inválidos, tente novamente\n")
        else:
            return n


def main():
    rodando = True
    while rodando:

        escolha = escolha_metodo()
        n = escolha_pontos(escolha)
        tipo = tabela_ou_funcao()

        if tipo == "F":
            f = ler_funcao()

            print("Insira o intervalo de integração [a; b]:")
            a = float(input("a: ").strip())
            b = float(input("b: ").strip())
            if a >= b:
                print("Erro: a deve ser menor que b. Tente novamente.")
                continue
        else:
            f = ler_tabela(n)
            a = f[0]
            b = f[n - 1]

        if escolha == "F":
            newton_cotes_fechadas(a, b, f, n)
        else:
            newton_cotes_abertas(a, b, f, n)

        rodando = input("\nDeseja continuar? (s/n) ").strip().lower() == "s"


main()
