import time
from datetime import datetime, timedelta

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITES_SAQUES = 3
TEMPO_BLOQUEIO = timedelta(hours=1)  # Após atingir o limite
intervalo_saque = 20  # Intervalo em segundos

ultimo_saque = datetime.min  # Data e hora do último saque
bloqueio_saque = None  

while True:
    opcao = input(menu)

    if opcao == "d":
        valor = float(input("Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso!")
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        if bloqueio_saque and datetime.now() < bloqueio_saque:
            print(f"Operação falhou! Você precisa aguardar até {bloqueio_saque.strftime('%H:%M:%S')} para poder realizar um novo saque.")
            continue

        valor = float(input("Informe o valor do saque: "))

        # Verificar se o tempo do saque anterior é suficiente
        tempo_decorrido = (datetime.now() - ultimo_saque).total_seconds()
        if tempo_decorrido < intervalo_saque:
            print(f"Operação falhou! Aguarde {intervalo_saque - tempo_decorrido:.0f} segundos antes de realizar outro saque.")
            continue

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITES_SAQUES

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente.")
        
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            bloqueio_saque = datetime.now() + TEMPO_BLOQUEIO
            print(f"Operação falhou! Número máximo de saques excedido. Aguardar até {bloqueio_saque.strftime('%H:%M:%S')} para poder realizar novos saques.")
        
        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            ultimo_saque = datetime.now()
            print("Saque realizado com sucesso!")
        
        else:
            print("Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")





