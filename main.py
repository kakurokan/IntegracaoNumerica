from sympy import symbols, parse_expr, E, lambdify
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
    convert_xor,
)


class n_nao_par(Exception):
    pass


class n_multiplo_de_3(Exception):
    pass


class fora_do_intervalo(Exception):
    pass


class precisa_ser_4(Exception):
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


def newton_cotes_fechadas(a, b, f, n):
    if n == 1:
        return trapezio_composto(a, b, f, n)
    elif n == 2:
        return regra_simpson(a, b, f, n)
    elif n == 3:
        return regra_simpson2(a, b, f, n)
    elif n == 4:
        return regra_boole(a, b, f, n)
    else:
        raise fora_do_intervalo

def trapezio_composto(x0, xn, f, n):
    h = (xn - x0) / n
    soma = f(x0) + f(xn)

    for i in range(1,n):
        xi = x0 + i * h
        soma += 2 * f(xi)

    IT = (h/2) * soma
    return IT

def regra_simpson(x0, xn, f, n):
    if n % 2 != 0:
        raise n_nao_par
    h = (xn - x0) / n
    soma = f(x0) + f(xn)

    for i in range(1, n, 2):
        soma += 4 * f(x0 + i * h)

    for i in range(2, n, 2):
        soma += 2 * f(x0 + i * h)

    IT = (h/3) * soma
    return IT

def regra_simpson2(x0, xn, f, n):
    if n % 3 != 0:
        raise n_multiplo_de_3

    h = (xn - x0) / n
    soma = f(x0) + f(xn)

    for i in range(1, n):
        xi = x0 + i * h
        if i % 3 == 0:
            soma += 2 * f(xi)
        else:
            soma += 3 * f(xi)

    IT = ((3*h)/8) * soma
    return IT

def regra_boole(x0, xn, f, n):
    if n != 4:
        raise precisa_ser_4
    h = (xn - x0) / n
    x1 = x0 + h
    x2 = x0 + 2*h
    x3 = x0 + 3*h
    return (2*h/45) * (7*f(x0) + 32*f(x1) + 12*f(x2) + 32*f(x3) + 7*f(xn))

def newton_cotes_abertas(a, b, f, n):
    h = (b - a) / (n + 2)
    x0 = a + h

    if n == 0:  # Ponto medio a guess
        return 2 * h * f(x0)
    elif n == 1:  # Não sei o nome
        x1 = x0 + h
        return ((3 * h) / 2) * (f(x0) + f(x1))
    elif n == 2:
        x1 = x0 + h
        x2 = x0 + 2 * h
        return ((4 * h) / 3) * (2 * f(x0) - f(x1) + 2 * f(x2))
    elif n == 3:
        x1 = x0 + h
        x2 = x0 + 2 * h
        x3 = x0 + 3 * h
        return (5 * h / 24) * (11 * f(x0) + f(x1) + f(x2) + 11 * f(x3))
    else:
        raise fora_do_intervalo


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
        f = ler_funcao()

        print("Insira o intervalo de integração [a; b]:")
        a = float(input("a: ").strip())
        b = float(input("b: ").strip())
        if a >= b:
            print("Erro: a deve ser menor que b. Tente novamente.")
            continue

        rodando = input("\nDeseja continuar? (s/n) ").strip().lower() == "s"


main()
