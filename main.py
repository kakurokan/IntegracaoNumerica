from sympy import symbols, parse_expr, E, lambdify, SympifyError, pi
from sympy.parsing.sympy_parser import (
    implicit_multiplication_application,
    standard_transformations,
    convert_xor,
)

FECHADAS = {
    1: "Regra do Trapézio",
    2: "Regra de Simpson",
    3: "Regra de Simpson dos 3/8",
    4: "Regra de Boole",
}
ABERTAS = {
    0: "Regra do Ponto Médio",
    1: "Regra para n = 1",
    2: "Regra de Milne",
    3: "Regra para n = 3",
}


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
    # Configuração para entender 'pi', 'e', '^', multiplicação implícita
    transformations = standard_transformations + (
        implicit_multiplication_application,
        convert_xor,
    )
    local_context = {"pi": pi, "e": E}

    expr = parse_expr(
        entrada, local_dict=local_context, transformations=transformations
    )

    return expr


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
        y0 = f[0]
        y1 = f[1]

    soma = y0 + y1
    return h / 2 * soma


def regra_simpson(x0, x2, f):
    h = (x2 - x0) / 2

    if callable(f):
        y0 = f(x0)
        y1 = f(x0 + h)
        y2 = f(x2)
    else:
        y0 = f[0]
        y1 = f[1]
        y2 = f[2]

    soma = y0 + 4 * y1 + y2

    return h / 3 * soma


def regra_simpson_3_8(x0, x3, f):
    h = (x3 - x0) / 3

    if callable(f):
        y0 = f(x0)
        y3 = f(x3)
    else:
        y0 = f[0]
        y3 = f[3]

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
        y4 = f(x4)
    else:
        y0 = f[0]
        y1 = f[1]
        y2 = f[2]
        y3 = f[3]
        y4 = f[4]

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
        y0 = f[0]

    return 2 * h * y0


def abertas_um(a, b, f):
    h = (b - a) / 3

    if callable(f):
        x0 = a + h
        x1 = b - h

        y0 = f(x0)
        y1 = f(x1)
    else:
        y0 = f[0]
        y1 = f[1]

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
        y0 = f[0]
        y1 = f[1]
        y2 = f[2]

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
        y0 = f[0]
        y1 = f[1]
        y2 = f[2]
        y3 = f[3]

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
    print(
        f"O método escolhido requer exatamente {n + 1} pontos.",
        "Insira os valores de f(x) (ou y) sequencialmente.",
    )

    pontos = []

    for i in range(n + 1):
        numero = ler_valor_matematico(input(f"Insira o ponto {i}: ").strip())
        pontos.append(float(numero.evalf()))

    return pontos


def ler_funcao():
    x = symbols("x", real=True)

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

    return f, f_exp, x


def escolha_pontos(tipo):
    while True:
        n = int(input("Insira o número de pontos: "))
        if (tipo == "F" and (n < 1 or n > 4)) or (tipo == "A" and (n < 0 or n > 3)):
            print("Pontos inválidos, tente novamente\n")
        else:
            return n


def verificar_extremos(var, a, b, f):
    try:
        fa = f.subs(var, a).evalf()
        fb = f.subs(var, b).evalf()

        if not fa.is_finite or not fa.is_real or not fb.is_finite or not fb.is_real:
            return False
        return True
    except Exception as e:
        print(f" [ERRO] Não foi possível calcular em {a} ou {b}: {e}")
        return False


def main():
    rodando = True

    print("*" * 65)
    print("   Bem-vindo a calculadora de integração numérica")
    print("*" * 65)

    while rodando:
        try:
            tipo = tabela_ou_funcao()

            if tipo == "F":
                f, f_exp, var = ler_funcao()
            else:
                escolha = escolha_metodo()
                n = escolha_pontos(escolha)
                f = ler_tabela(n)

            print("Insira o intervalo de integração [a; b]:")
            a = ler_valor_matematico(input("Limite inferior (a): ").strip())
            b = ler_valor_matematico(input("Limite superior (b): ").strip())
            if a >= b:
                print("Erro: a deve ser menor que b. Tente novamente.")
                continue

            if tipo == "F":
                if not verificar_extremos(var, a, b, f_exp):
                    print(
                        "\nA função inserida não é válida nos limites fornecidos.\n",
                        "Não é possível utilizar as fórmulas de Newton-Cotes fechadas.\n",
                    )
                    escolha = "A"
                else:
                    escolha = escolha_metodo()

                n = escolha_pontos(escolha)

            a = float(a.evalf())
            b = float(b.evalf())

            if escolha == "F":
                resultado = newton_cotes_fechadas(a, b, f, n)
            else:
                resultado = newton_cotes_abertas(a, b, f, n)

            print(
                "RESULTADO FINAL:",
                (
                    "\nMétodo: " + FECHADAS.get(n)
                    if (escolha == "F")
                    else ABERTAS.get(n)
                ),
                "\nValor final: " + str(resultado),
            )

            rodando = input("\nDeseja continuar? (s/n) ").strip().lower() == "s"

        except SympifyError as e:
            print(f"Erro de sintaxe: {e}")
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Erro inesperado: {e}")


main()
