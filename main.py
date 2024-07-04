import PySimpleGUI as sg

sg.theme("DarkBlue17")


# GUI -> GRAPHIC USER INTERFACE

def menu():
    layoutMenu = [
        [sg.Image("logo.png")],
        [sg.Text("SEJA BEM VINDO AO APP")],
        [sg.Button("LOGIN")],
        [sg.Button("REGISTRAR")],
        [sg.Button("SAIR")],
    ]
    return sg.Window("Menu", layout=layoutMenu, finalize=True, size=(500, 300), element_justification='center')


def registrar():
    layoutRegistrar = [
        [sg.Text("SESSÃO DE CADASTRO")],
        [sg.Text("USUÁRIO: "), sg.Input(key="usuario")],
        [sg.Text("SENHA: "), sg.Input(key="senha", password_char="*")],
        [sg.Checkbox("CLIENTE", key="cliente", enable_events=True),
         sg.Checkbox("VENDEDOR", key="vendedor", enable_events=True)],
        [sg.Button("REGISTRAR")],
        [sg.Button("VOLTAR")]
    ]
    return sg.Window("Registrar", layout=layoutRegistrar, finalize=True, size=(500, 300),
                     element_justification='center')

def login():
    layoutLogin = [
    [sg.Text("SESSÃO DE LOGIN")],
    [sg.Text("Usuário: "), sg.Input(key="usuario")],
    [sg.Text("Senha: "), sg.Input(key="senha")],        
    [sg.Button("LOGIN")],
    [sg.Button("VOLTAR")]
    ]
    return sg.Window("Login", layout=layoutLogin, finalize=True, size=(500, 300),element_justification='center')


def registrarConta(usuario, senha, tipoConta):
    with open("usuario.txt", "r") as arquivo_usuario, open("senha.txt", "r") as arquivo_senha:
        usuarios = arquivo_usuario.readlines()
        senhas = arquivo_senha.readlines()

    if usuario + "\n" in usuarios or senha + "\n" in senhas:
        sg.popup("Login e senha inválidos, essas credenciais já existem")
    else:
        with open("usuario.txt", "a") as arquivo_usuario, open("senha.txt", "a") as arquivo_senha, open("tipoConta.txt",
                                                                                                        "a") as arquivo_tipoConta:
            arquivo_usuario.write(usuario + "\n")
            arquivo_senha.write(senha + "\n")
            arquivo_tipoConta.write(tipoConta + "\n")
        sg.popup("Cadastrado com sucesso!")

janelaMenu, janelaRegistro, janelaLogin = menu(), None, None

while True:
    window, event, values = sg.read_all_windows()

    if (window == janelaRegistro or window == janelaMenu or window == janelaLogin) and (event == sg.WINDOW_CLOSED or event == "SAIR"):
        break

    if window == janelaMenu and event == "LOGIN":
        janelaMenu.hide()
        janelaLogin = login()   
    if window == janelaMenu and event == "REGISTRAR":
        janelaMenu.hide()
        janelaRegistro = registrar()
    if window == janelaRegistro and event == "REGISTRAR":
        user = values["usuario"]
        password = values["senha"]
        if not values["cliente"] and not values["vendedor"]:
            sg.popup("Você deve selecionar pelo menos uma caixa.", title="Erro")
        else:
            tipoConta = "CLIENTE" if values["cliente"] else "VENDEDOR" if values["vendedor"] else ""
            registrarConta(user, password, tipoConta)

    if window == janelaRegistro and event == "VOLTAR":
        janelaRegistro.hide()
        janelaMenu.un_hide()
    
    if window == janelaLogin and event == "VOLTAR":
        janelaLogin.hide()
        janelaMenu.un_hide()

    if window == janelaRegistro and event == "cliente":
        if values["cliente"]:
            window["vendedor"].update(value=False)
    elif window == janelaRegistro and event == "vendedor":
        if values["vendedor"]:
            window["cliente"].update(value=False)

janelaMenu.close()

