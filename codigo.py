#Tela inicial
    #Título: HashZapp
    #Botão: "Iniciar Chat"
    #Ao clicar no botão: 
        #Abrir um popup:
            #Título: Bem vindo(a) ao HashZapp
            #Caixa de texto: Escreva seu nome
            #Botão: Entrar no chat
            #Ao clicar no botão:
                #Sumir com o título
                #Carregar o campo de enviar mensagem: "Digite sua mensagem"
                #Botão "Enviar"
                #Quando clicar no botão:
                    #Enviar a mensagem
                    #Limpar a caixa de mensagem

import flet as ft
def main(pagina):
    titulo = ft.Text('HashZapp')

    chat = ft.Column()

    nome_usuario = ft.TextField(label='Escreva seu nome:')

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem['tipo']
        if tipo == 'mensagem':
            texto_mensagem = mensagem['texto']
            usuario_mensagem = mensagem['usuario']
            #Adiciona a mensagem ao chat
            chat.controls.append(ft.Text(f'{usuario_mensagem}: {texto_mensagem}'))
        else:
            usuario_mensagem = mensagem['usuario']
            chat.controls.append(ft.Text(f'{usuario_mensagem} entrou no chat', size=12, italic=True,color=ft.colors.ORANGE_500))
            pagina.update()

    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({'texto': campo_mensagem.value, 'usuario': nome_usuario.value, 'tipo': 'mensagem'})
        campo_mensagem.value = '' #para limpar o campo de mensagem após o envio 
        pagina.update()

    campo_mensagem = ft.TextField(label='Digite sua mensagem', on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton('Enviar', on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({'usuario':nome_usuario.value, 'tipo':'entrada'})
        pagina.add(chat) #Adiciona o chat na página
        popup.open=False #Fecha o popup
        pagina.remove(botao) #Remove o botao_iniciar
        pagina.remove(titulo) #Remove o título
        pagina.add(ft.Row([campo_mensagem, botao_enviar_mensagem])) #Adiciona o campo de mensagem e o botão enviar_mensagem um ao lado do outro
        pagina.update() 

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text('Bem vindo(a) ao HashZapp!'),
        content = nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click = entrar_popup)]
        )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open=True
        pagina.update()

    botao = ft.ElevatedButton('Iniciar Chat', on_click=entrar_chat)
    pagina.add(titulo)
    pagina.add(botao)

ft.app(main, view=ft.WEB_BROWSER, port= 8000)