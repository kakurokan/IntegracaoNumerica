from sympy import symbols, parse_expr, E, lambdify, SympifyError, pi
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


def ler_valor_matematico(entrada):
    while True:
        # Configuração para entender 'pi', 'e', '^', multiplicação implícita
        transformations = standard_transformations + (
            implicit_multiplication_application,
            convert_xor,
        )
        local_context = {"pi": pi, "e": E}

        try:
            expr = parse_expr(
                entrada, local_dict=local_context, transformations=transformations
            )

            # 2. Avalia a expressão para um número real (float)
            valor_float = float(expr.evalf())

            return valor_float

        except Exception as e:
            print(f"Entrada inválida ({entrada}). Tente algo como 'pi', 'pi/2', '1.5'.")


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

    if callable(f):
        y0 = f(x0)
        y1 = f(x1)
    else:
        y0 = x0
        y1 = x1

    soma = y0 + y1
    return h / 2 * soma


def regra_simpson(x0, x2, f):
    h = (x2 - x0) / 2

    if callable(f):
        y0 = f(x0)
        y1 = f(x0 + h)
        y2 = f(x2)
    else:
        y0 = x0
        y1 = f[1]
        y2 = x2

    soma = y0 + 4 * y1 + y2

    return h / 3 * soma


def regra_simpson_3_8(x0, x3, f):
    h = (x3 - x0) / 3

    if callable(f):
        y0 = f(x0)
        y3 = f(x3)
    else:
        y0 = x0
        y3 = x3

    soma = y0 + y3

    for i in range(1, 3):
        if callable(f):
            yi = f(x0 + i * h)
        else:
            yi = f[i]

        soma += 3 * yi

    return 3 * h / 8 * soma


def regra_boole(x0, x4, f):
    h = (x4 - x0) / 4

    if callable(f):
        y0 = f(x0)
        y1 = f(x0 + h)
        y2 = f(x0 + 2 * h)
        y3 = f(x0 + 3 * h)
    else:
        y0 = x0
        y1 = f[1]
        y2 = f[2]
        y3 = f[3]
        y4 = x4

    soma = 7 * y0 + 32 * y1 + 12 * y2 + 32 * y3 + 7 * y4
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
    h = (b - a) / 2

    if callable(f):
        y0 = f(a + h)
    else:
        y0 = f[1]

    return 2 * h * y0


def abertas_um(a, b, f):
    h = (b - a) / 3

    if callable(f):
        x0 = a + h
        x1 = b - h

        y0 = f(x0)
        y1 = f(x1)
    else:
        y0 = f[1]
        y1 = f[2]

    soma = y0 + y1
    return 3 * h / 2 * soma


def regra_milne(a, b, f):
    h = (b - a) / 4

    if callable(f):
        x0 = a + h
        x1 = x0 + h
        x2 = b - h

        y0 = f(x0)
        y1 = f(x1)
        y2 = f(x2)
    else:
        y0 = f[1]
        y1 = f[2]
        y2 = f[3]

    soma = 2 * y0 - y1 + 2 * y2
    return 4 * h / 3 * soma


def abertas_tres(a, b, f):
    h = (b - a) / 5

    if callable(f):
        x0 = a + h
        x1 = x0 + h
        x2 = x0 + h * 2
        x3 = b - h

        y0 = f(x0)
        y1 = f(x1)
        y2 = f(x2)
        y3 = f(x3)
    else:
        y0 = f[1]
        y1 = f[2]
        y2 = f[3]
        y3 = f[4]

    soma = 11 * y0 + y1 + y2 + 11 * y3
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
    print(f"Insira os valores da tabela com {n} pontos equidistantes")

    pontos = []

    for i in range(n):
        numero = float(input(f"Insira o ponto {i}: ").strip())
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
        "pi": pi,
    }  # Permite que o parse reconhece e = exp() e x como variável
    f_exp = parse_expr(
        f, local_dict=locals_vars, transformations=transformations
    )  # Converte o input numa expressão sympy
    f = lambdify(x, f_exp, modules="math")  # Converte a função em método

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

        try:
            escolha = escolha_metodo()
            n = escolha_pontos(escolha)
            tipo = tabela_ou_funcao()

            if tipo == "F":
                f = ler_funcao()

                print("Insira o intervalo de integração [a; b]:")
                a = ler_valor_matematico(input("a: ").strip())
                b = ler_valor_matematico(input("b: ").strip())
                if a >= b:
                    print("Erro: a deve ser menor que b. Tente novamente.")
                    continue
            else:
                f = ler_tabela(n)
                a = f[0]
                b = f[n - 1]

            if escolha == "F":
                resultado = newton_cotes_fechadas(a, b, f, n)
            else:
                resultado = newton_cotes_abertas(a, b, f, n)

            print("O resultado aproximado para integral é: " + str(resultado))

            rodando = input("\nDeseja continuar? (s/n) ").strip().lower() == "s"

        except SympifyError as e:
            print(f"Erro de sintaxe: {e}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Erro inesperado: {e}")


main()
