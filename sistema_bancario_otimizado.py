import os

# Limpar a tela
def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para obter todas as contas disponíveis
def obter_contas_disponiveis(saldo, extrato, saques_diarios):
    todas_contas = set(saldo.keys()) | set(extrato.keys()) | set(saques_diarios.keys())
    return list(todas_contas)

# Função que inicializa os valores de saldo, extrato e saques diários para uma nova conta
def inicializar_conta(numero_conta, saldo, extrato, saques_diarios):
    saldo[numero_conta] = 0
    extrato[numero_conta] = ""
    saques_diarios[numero_conta] = 0

# Função para depósito
def deposito(valor, saldo, extrato, usuario_contas):
    for i, conta_numero in enumerate(usuario_contas, start=1):
        print(f"{i}. Conta número: {conta_numero}")
    escolha_conta = int(input("Escolha a conta para depósito: ")) - 1
    if 0 <= escolha_conta < len(usuario_contas):
        conta_escolhida = usuario_contas[escolha_conta]
        if valor > 0:
            saldo[conta_escolhida] = saldo.get(conta_escolhida, 0) + valor
            extrato[conta_escolhida] = extrato.get(conta_escolhida, "") + f"Depósito: +R${valor:.2f}\n"
            print(f"Depósito de R${valor:.2f} realizado com sucesso na conta número {conta_escolhida}.")
        else:
            print("Valor de depósito deve ser positivo.")
    else:
        print("Conta Inexistente.")

# Função para saque
def saque(*, valor, saldo, extrato, saques_diarios, LIMITE_SAQUES, LIMITE_SAQUE_VALOR, usuario_contas):
    for i, conta_numero in enumerate(usuario_contas, start=1):
        print(f"{i}. Conta número: {conta_numero}")
    escolha_conta = int(input("Escolha a conta para saque: ")) - 1
    if 0 <= escolha_conta < len(usuario_contas):
        conta_escolhida = usuario_contas[escolha_conta]
        if saques_diarios.get(conta_escolhida, 0) < LIMITE_SAQUES:
            if valor > 0:
                if valor <= LIMITE_SAQUE_VALOR:
                    if valor <= saldo.get(conta_escolhida, 0):
                        saldo[conta_escolhida] -= valor
                        extrato[conta_escolhida] = extrato.get(conta_escolhida, "") + f"Saque: -R${valor:.2f}\n"
                        saques_diarios[conta_escolhida] = saques_diarios.get(conta_escolhida, 0) + 1
                        print(f"Saque de R${valor:.2f} realizado com sucesso na conta número {conta_escolhida}.")
                    else:
                        print("Saldo insuficiente para saque.")
                else:
                    print(f"O valor máximo para saque é R${LIMITE_SAQUE_VALOR:.2f}.")
            else:
                print("Valor de saque deve ser positivo.")
        else:
            print(f"Limite de 3 saques diários atingido para a conta número {conta_escolhida}.")
    else:
        print("Conta Inexistente.")

# Função para exibir o extrato
def exibir_extrato(saldo, *, extrato, usuario_contas):
    for i, conta_numero in enumerate(usuario_contas, start=1):
        print(f"{i}. Conta número: {conta_numero}")
    escolha_conta = int(input("Escolha a conta para extrato: ")) - 1
    if 0 <= escolha_conta < len(usuario_contas):
        conta_escolhida = usuario_contas[escolha_conta]
        print("\n--- Extrato ---")
        if extrato[conta_escolhida]:
            print(extrato[conta_escolhida])
        else:
            print("Nenhuma operação realizada.")
        print(f"Saldo atual da conta número {conta_escolhida}: R${saldo[conta_escolhida]:.2f}")
    else:
        print("Conta Inexistente.")

# Função para cadastrar um usuário
def cadastrar_usuario(usuarios):
    cpf = input("Digite o CPF (somente números): ")
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            print("Usuário com este CPF já cadastrado.")
            return usuarios
    nome = input("Digite o nome: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/yyyy): ")
    endereco = input("Digite o endereço (logradouro - nº - bairro - cidade/UF): ")
    usuarios.append({
        'nome': nome,
        'cpf': cpf,
        'data_nascimento': data_nascimento,
        'endereco': endereco,
        'contas': []
    })
    print("Usuário cadastrado com sucesso.")
    return usuarios

# Função para cadastrar uma conta
def cadastrar_conta(contas, usuarios, numero_conta, saldo, extrato, saques_diarios):
    cpf = input("Digite o CPF do usuário: ")
    usuario_encontrado = None
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            usuario_encontrado = usuario
            break
    if not usuario_encontrado:
        print("Usuário não encontrado.")
        return contas, numero_conta
    # Verifica se o usuário já possui a conta cadastrada
    for conta in contas:
        if conta['usuario'] == usuario_encontrado:
            print("Este usuário já possui uma conta cadastrada.")
            return contas, numero_conta
    # Se o usuário não possui uma conta cadastrada, adiciona a nova conta
    contas.append({
        'agencia': '0001',
        'numero_conta': numero_conta,
        'usuario': usuario_encontrado
    })
    usuario_encontrado['contas'].append(numero_conta)
    print("Conta cadastrada com sucesso.")
    # Inicializa os valores de saldo, extrato e saques diários para a nova conta
    inicializar_conta(numero_conta, saldo, extrato, saques_diarios)
    return contas, numero_conta + 1

# Função para listar contas
def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        usuario = conta['usuario']
        print(f"Agência: {conta['agencia']} - Número da Conta: {conta['numero_conta']} - Usuário: {usuario['nome']} - CPF: {usuario['cpf']}")

# Função para listar usuários e suas contas
def listar_usuarios(usuarios):
    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return
    for usuario in usuarios:
        print(f"Nome: {usuario['nome']} - CPF: {usuario['cpf']} - Endereço: {usuario['endereco']}")
        if usuario['contas']:
            print("Contas:")
            for conta_numero in usuario['contas']:
                print(f"- Conta número: {conta_numero}")
        else:
            print("Nenhuma conta cadastrada para este usuário.")

# Função principal
def main():
    usuarios = []
    contas = []  
    numero_conta = 1

    saldo = {}  # Dicionário para armazenar o saldo de cada conta
    extrato = {}  # Dicionário para armazenar o extrato de cada conta
    saques_diarios = {}  # Dicionário para armazenar o número de saques diários de cada conta
    LIMITE_SAQUES = 3  
    LIMITE_SAQUE_VALOR = 500.0  

    while True:
        limpar_tela()
        print("\n--- Menu Inicial ---")
        print("1. Cadastros")
        print("2. Serviços Bancários")
        print("3. Sair")

        opcao_menu_inicial = input("Escolha uma opção: ")

        if opcao_menu_inicial == '1':
            while True:
                limpar_tela()
                print("\n--- Menu Cadastros ---")
                print("1. Cadastrar Usuário")
                print("2. Cadastrar Conta")
                print("3. Listar Contas")
                print("4. Usuários Cadastrados")
                print("5. Voltar para o menu anterior")

                opcao_cadastros = input("Escolha uma opção: ")

                if opcao_cadastros == '1':
                    usuarios = cadastrar_usuario(usuarios)
                elif opcao_cadastros == '2':
                    contas, numero_conta = cadastrar_conta(contas, usuarios, numero_conta, saldo, extrato, saques_diarios)
                elif opcao_cadastros == '3':
                    listar_contas(contas)
                elif opcao_cadastros == '4':
                    listar_usuarios(usuarios)
                elif opcao_cadastros == '5':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

        elif opcao_menu_inicial == '2':
            while True:
                limpar_tela()
                print("\n--- Menu Serviços Bancários ---")
                print("1. Depósito")
                print("2. Saque")
                print("3. Extrato")
                print("4. Voltar para o menu anterior")

                opcao_servicos_bancarios = input("Escolha uma opção: ")

                todas_contas = obter_contas_disponiveis(saldo, extrato, saques_diarios)

                if opcao_servicos_bancarios == '1':
                    valor_deposito = float(input("Digite o valor a ser depositado: "))
                    deposito(valor=valor_deposito, saldo=saldo, extrato=extrato, usuario_contas=todas_contas)
                elif opcao_servicos_bancarios == '2':
                    valor_saque = float(input("Digite o valor a ser sacado: "))
                    saque(valor=valor_saque, saldo=saldo, extrato=extrato, saques_diarios=saques_diarios, LIMITE_SAQUES=LIMITE_SAQUES, LIMITE_SAQUE_VALOR=LIMITE_SAQUE_VALOR, usuario_contas=todas_contas)
                elif opcao_servicos_bancarios == '3':
                    exibir_extrato(saldo=saldo, extrato=extrato, usuario_contas=todas_contas)
                elif opcao_servicos_bancarios == '4':
                    break
                else:
                    print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")

# Chamada da função main() se o script for executado diretamente
if __name__ == "__main__":
    main()



