import re
from datetime import datetime

# Função para validar o número do cartão de crédito usando o Algoritmo de Luhn
def validar_numero_cartao(numero_cartao):

    numero_cartao = numero_cartao.replace(' ', '')

    if not re.match(r'^\d{16}$', numero_cartao):

        return False

    soma = 0
    inverso = numero_cartao[::-1]

    for i, digito in enumerate(inverso):

        n = int(digito)

        if i % 2 == 1:

            n *= 2

            if n > 9:

                n -= 9

        soma += n

    return soma % 10 == 0

def validar_data_validade(data_validade_str):

    try:

        data_validade = datetime.strptime(data_validade_str, '%m/%Y')

    except ValueError:

        data_validade = datetime.strptime(data_validade_str, '%m/%y')

    hoje = datetime.now()

    return data_validade > hoje

def validar_cvv(cvv):

    return re.match(r'^\d{3,4}$', cvv) is not None

def validar_dados_pagamento(numero_cartao, data_validade_str, cvv):

    if not validar_numero_cartao(numero_cartao):

        return False

    if not validar_data_validade(data_validade_str):

        return False

    if not validar_cvv(cvv):

        return False

    return True
