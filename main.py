import os
import datetime
import json

tarefas = []

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def adicionar_tarefa():
    limpar_tela()
    descricao = input("Descrição da tarefa: ")
    prioridade = input("Prioridade (alta, media, baixa): ").lower()
    if prioridade not in ['alta', 'media', 'baixa']:
        print("Prioridade inválida.")
        return
    data_criacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "pendente"
    tarefa = {
        "descricao": descricao,
        "prioridade": prioridade,
        "status": status,
        "data_criacao": data_criacao,
        "data_conclusao": None
    }
    tarefas.append(tarefa)
    print("Tarefa adicionada com sucesso!")

def listar_tarefas():
    limpar_tela()
    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return
    for index, tarefa in enumerate(tarefas, 1):
        print(f"{index}. {tarefa['descricao']} | Prioridade: {tarefa['prioridade']} | Status: {tarefa['status']} | Criada em: {tarefa['data_criacao']}")

def editar_tarefa():
    listar_tarefas()
    try:
        id_tarefa = int(input("\nDigite o número da tarefa que deseja editar: "))
        if id_tarefa < 1 or id_tarefa > len(tarefas):
            print("Tarefa não encontrada.")
            return
        tarefa = tarefas[id_tarefa - 1]
        descricao = input(f"Descrição atual: {tarefa['descricao']}\nNova descrição: ")
        prioridade = input(f"Prioridade atual: {tarefa['prioridade']}\nNova prioridade (alta, media, baixa): ").lower()
        if prioridade not in ['alta', 'media', 'baixa']:
            print("Prioridade inválida.")
            return
        tarefa['descricao'] = descricao
        tarefa['prioridade'] = prioridade
        print("Tarefa editada com sucesso!")
    except ValueError:
        print("Entrada inválida.")

def remover_tarefa():
    listar_tarefas()
    try:
        id_tarefa = int(input("\nDigite o número da tarefa que deseja remover: "))
        if id_tarefa < 1 or id_tarefa > len(tarefas):
            print("Tarefa não encontrada.")
            return
        tarefas.pop(id_tarefa - 1)
        print("Tarefa removida com sucesso!")
    except ValueError:
        print("Entrada inválida.")

def marcar_concluida():
    listar_tarefas()
    try:
        id_tarefa = int(input("\nDigite o número da tarefa que deseja marcar como concluída: "))
        if id_tarefa < 1 or id_tarefa > len(tarefas):
            print("Tarefa não encontrada.")
            return
        tarefa = tarefas[id_tarefa - 1]
        if tarefa['status'] == "concluída":
            print("Tarefa já está concluída.")
            return
        tarefa['status'] = "concluída"
        tarefa['data_conclusao'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Tarefa marcada como concluída!")
    except ValueError:
        print("Entrada inválida.")

def salvar_tarefas():
    with open("tarefas.json", "w") as file:
        json.dump(tarefas, file)

def carregar_tarefas():
    global tarefas
    try:
        with open("tarefas.json", "r") as file:
            tarefas = json.load(file)
    except FileNotFoundError:
        tarefas = []

def menu():
    carregar_tarefas()
    while True:
        limpar_tela()
        print("Menu:")
        print("1. Adicionar tarefa")
        print("2. Listar tarefas")
        print("3. Editar tarefa")
        print("4. Remover tarefa")
        print("5. Marcar tarefa como concluída")
        print("6. Sair")
        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            adicionar_tarefa()
        elif escolha == "2":
            listar_tarefas()
        elif escolha == "3":
            editar_tarefa()
        elif escolha == "4":
            remover_tarefa()
        elif escolha == "5":
            marcar_concluida()
        elif escolha == "6":
            salvar_tarefas()
            print("Tarefas salvas. Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")
        input("\nPressione Enter para continuar...")

menu()
