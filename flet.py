import flet as ft
import datetime
import json

tarefas = []

def carregar_tarefas():
    global tarefas
    try:
        with open("tarefas.json", "r") as file:
            tarefas = json.load(file)
    except FileNotFoundError:
        tarefas = []

def salvar_tarefas():
    with open("tarefas.json", "w") as file:
        json.dump(tarefas, file)

def adicionar_tarefa(descricao, prioridade):
    if prioridade not in ['alta', 'media', 'baixa']:
        return "Prioridade inválida"
    data_criacao = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tarefa = {"descricao": descricao, "prioridade": prioridade, "status": "pendente", "data_criacao": data_criacao, "data_conclusao": None}
    tarefas.append(tarefa)
    return f"Tarefa '{descricao}' adicionada com sucesso!"

def listar_tarefas():
    if not tarefas:
        return ["Nenhuma tarefa cadastrada."]
    return [f"{index+1}. {t['descricao']} | Prioridade: {t['prioridade']} | Status: {t['status']} | Criada em: {t['data_criacao']}" for index, t in enumerate(tarefas)]

def editar_tarefa(id_tarefa, descricao, prioridade):
    if id_tarefa < 1 or id_tarefa > len(tarefas):
        return "Tarefa não encontrada."
    if prioridade not in ['alta', 'media', 'baixa']:
        return "Prioridade inválida."
    tarefa = tarefas[id_tarefa - 1]
    tarefa['descricao'] = descricao
    tarefa['prioridade'] = prioridade
    return "Tarefa editada com sucesso!"

def remover_tarefa(id_tarefa):
    if id_tarefa < 1 or id_tarefa > len(tarefas):
        return "Tarefa não encontrada."
    tarefas.pop(id_tarefa - 1)
    return "Tarefa removida com sucesso!"

def marcar_concluida(id_tarefa):
    if id_tarefa < 1 or id_tarefa > len(tarefas):
        return "Tarefa não encontrada."
    tarefa = tarefas[id_tarefa - 1]
    if tarefa['status'] == "concluída":
        return "Tarefa já está concluída."
    tarefa['status'] = "concluída"
    tarefa['data_conclusao'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "Tarefa marcada como concluída."

def main(page: ft.Page):
    page.title = "Gerenciador de Tarefas"
    page.vertical_alignment = ft.MainAxisAlignment.START

    tarefa_list = ft.Column()
    carregar_tarefas()

    descricao_input = ft.TextField(label="Descrição da tarefa", autofocus=True)
    prioridade_input = ft.TextField(label="Prioridade (alta, media, baixa)")
    feedback_text = ft.Text()

    def atualizar_lista():
        tarefa_list.controls.clear()
        tarefa_list.controls.extend([ft.Text(tarefa) for tarefa in listar_tarefas()])
        page.update()

    def on_adicionar_click(e):
        descricao = descricao_input.value
        prioridade = prioridade_input.value.lower()
        mensagem = adicionar_tarefa(descricao, prioridade)
        feedback_text.value = mensagem
        atualizar_lista()
        descricao_input.value = ""
        prioridade_input.value = ""
        page.update()

    def on_listar_click(e):
        atualizar_lista()
        page.update()

    def on_editar_click(e):
        try:
            id_tarefa = int(descricao_input.value)
            descricao = descricao_input.value
            prioridade = prioridade_input.value.lower()
            mensagem = editar_tarefa(id_tarefa, descricao, prioridade)
            feedback_text.value = mensagem
        except ValueError:
            feedback_text.value = "ID inválido."
        atualizar_lista()
        descricao_input.value = ""
        prioridade_input.value = ""
        page.update()

    def on_remover_click(e):
        try:
            id_tarefa = int(descricao_input.value)
            mensagem = remover_tarefa(id_tarefa)
            feedback_text.value = mensagem
        except ValueError:
            feedback_text.value = "ID inválido."
        atualizar_lista()
        descricao_input.value = ""
        prioridade_input.value = ""
        page.update()

    def on_concluir_click(e):
        try:
            id_tarefa = int(descricao_input.value)
            mensagem = marcar_concluida(id_tarefa)
            feedback_text.value = mensagem
        except ValueError:
            feedback_text.value = "ID inválido."
        atualizar_lista()
        descricao_input.value = ""
        prioridade_input.value = ""
        page.update()

    def on_sair_click(e):
        salvar_tarefas()
        feedback_text.value = "Tarefas salvas. Saindo..."
        page.update()

    page.add(
        ft.Column(
            [
                descricao_input,
                prioridade_input,
                ft.Row(
                    [
                        ft.ElevatedButton("Adicionar Tarefa", on_click=on_adicionar_click),
                        ft.ElevatedButton("Listar Tarefas", on_click=on_listar_click),
                        ft.ElevatedButton("Editar Tarefa", on_click=on_editar_click),
                        ft.ElevatedButton("Remover Tarefa", on_click=on_remover_click),
                        ft.ElevatedButton("Marcar Concluída", on_click=on_concluir_click),
                        ft.ElevatedButton("Sair", on_click=on_sair_click),
                    ]
                ),
                feedback_text,
                tarefa_list,
            ]
        )
    )

ft.app(target=main)
