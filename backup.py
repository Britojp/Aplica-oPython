import PySimpleGUI as sg

sg.theme("DarkBlue17")

# GUI -> INTERFACE GRÁFICA DO USUÁRIO

def menu():
    layoutMenu = [
        [sg.Image("logo.png")],
        [sg.Text("SEJA BEM-VINDO AO APP")],
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
        [sg.Text("USUÁRIO: "), sg.Input(key="usuario")],
        [sg.Text("SENHA: "), sg.Input(key="senha", password_char="*")],
        [sg.Button("LOGIN")],
        [sg.Button("VOLTAR")]
    ]
    return sg.Window("Login", layout=layoutLogin, finalize=True, size=(500, 300), element_justification='center')

def telaVendedor(produtos, saldo):
    layoutProdutos = [
        [sg.Image(produto[0]), sg.Text(produto[1])]
        for produto in produtos
    ]
    layoutVendedor = [
        [sg.Text("Seja bem-vindo!")],
        [sg.Text(f"Seu saldo é de: {saldo} R$")],
        [sg.Text("Abaixo estão dispostos os produtos já postados")],
        [sg.Button("ADICIONAR PRODUTOS")],
        [sg.Button("VOLTAR")],
        [sg.Column(layoutProdutos, scrollable=True, vertical_scroll_only=True, size=(480, 200))],
    ]
    return sg.Window("Vendedor", layout=layoutVendedor, finalize=True, size=(500, 300), element_justification='center')

def telaComprador(produtos, saldo):
    layoutProdutos = [
        [sg.Image(produto[0]), sg.Text(produto[1]), sg.Button("Comprar", key=f"comprar_{indice}")]
        for indice, produto in enumerate(produtos)
    ]
    layoutComprador = [
        [sg.Text("Bem-vindo à loja!")],
        [sg.Text("Aqui você pode comprar produtos disponíveis.")],
        [sg.Button("Adicionar saldo")],
        [sg.Button("Consultar saldo")],
        [sg.Button("VOLTAR")],
        [sg.Column(layoutProdutos, scrollable=True, vertical_scroll_only=True, size=(480, 200))]
    ]
    return sg.Window("Comprador", layout=layoutComprador, finalize=True, size=(500, 300), element_justification='center')

def adicionarProduto():
    layoutAdicionarProduto = [
        [sg.Text("Adicionar Novo Produto")],
        [sg.Text("Nome do Produto: "), sg.Input(key="nome_produto")],
        [sg.Text("Valor do Produto: "), sg.Input(key="valor_produto")],
        [sg.Text("Imagem"), sg.Input(key="FILE"), sg.FileBrowse()],
        [sg.Button("ADICIONAR"), sg.Button("VOLTAR")]
    ]
    return sg.Window("Adicionar Produto", layout=layoutAdicionarProduto, finalize=True, size=(500, 200), element_justification='center')

def adicionarSaldo():
    layoutSaldo = [
        [sg.Text("Digite o valor que deseja inserir")],
        [sg.Input(key='saldo')],
        [sg.Button('OK'), sg.Button('VOLTAR')]
    ]
    return sg.Window("Adicionar saldo", layout=layoutSaldo, finalize=True, size=(500, 200), element_justification='center')


def registrarConta(usuario, senha, tipoConta):
    with open("usuario.txt", "r") as arquivo_usuario, open("senha.txt", "r") as arquivo_senha:
        usuarios = arquivo_usuario.readlines()
        senhas = arquivo_senha.readlines()

    if usuario + "\n" in usuarios or senha + "\n" in senhas:
        sg.popup("Login e senha inválidos, essas credenciais já existem")
    else:
        with open("usuario.txt", "a") as arquivo_usuario, open("senha.txt", "a") as arquivo_senha, open("tipoConta.txt", "a") as arquivo_tipoConta:
            arquivo_usuario.write(usuario + "\n")
            arquivo_senha.write(senha + "\n")
            arquivo_tipoConta.write(tipoConta + "\n")
        sg.popup("Cadastrado com sucesso!")

def verificarConta(user, password):
    with open("usuario.txt", "r") as arquivo_usuario, \
         open("senha.txt", "r") as arquivo_senha, \
         open("tipoConta.txt", "r") as arquivo_tipoConta:

        usuarios = [linha.strip() for linha in arquivo_usuario.readlines()]
        senhas = [linha.strip() for linha in arquivo_senha.readlines()]
        tipoContas = [linha.strip() for linha in arquivo_tipoConta.readlines()]

    if user in usuarios:
        indice = usuarios.index(user)
        if senhas[indice] == password:
            tipoConta = tipoContas[indice]
            sg.popup(f"Bem-vindo, {user}! Tipo de conta: {tipoConta}")
            return tipoConta
        else:
            sg.popup("Credenciais inválidas, tente novamente")
            return None
    else:
        sg.popup("Usuário não encontrado")
        return None

def buscarValorProduto(indice_produto, produtos):
    return produtos[indice_produto][1].split(": ")[1].split(" R$")[0]

def realizarCompra(indice_produto, produtos, saldo):
    global valor_produto
    valor_produto = float(buscarValorProduto(indice_produto, produtos))
    if saldo >= valor_produto:
        saldo -= valor_produto
        sg.popup(f"Compra realizada com sucesso! Seu novo saldo é de {saldo} R$")
    else:
        sg.popup("Saldo insuficiente para realizar a compra.")

produtos = [
    ["giftcardsteam.png", "Valor: 50 R$"],
    ["lolgiftcard.png", "Valor: 50 R$"],
    ["robloxgiftcard.png", "Valor: 50 R$"],
]
saldo = 0
valor_produto = 0
saldo_vendedor = 0
janelaMenu, janelaRegistro, janelaSaldo, janelaLogin, janelaVendedor, janelaComprador, janelaAdicionarProduto = menu(), None, None, None, None, None, None

while True:
    window, event, values = sg.read_all_windows()

    if window == janelaMenu and event == "SAIR":
        sg.popup("Obrigado por usar o app!")
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
            sg.popup("Você deve selecionar pelo menos uma opção.", title="Erro")
        else:
            tipoConta = "CLIENTE" if values["cliente"] else "VENDEDOR" if values["vendedor"] else ""
            registrarConta(user, password, tipoConta)
            janelaRegistro.hide()
            janelaMenu.un_hide()
    if window == janelaRegistro and event == "VOLTAR":
        janelaRegistro.hide()
        janelaMenu.un_hide()

    if window == janelaLogin and event == "VOLTAR":
        janelaLogin.hide()
        janelaMenu.un_hide()

    if event == "cliente" and values["cliente"]:
        janelaRegistro["vendedor"].update(value=False)

    if event == "vendedor" and values["vendedor"]:
        janelaRegistro["cliente"].update(value=False)

    if window == janelaLogin and event == "LOGIN":
        user = values["usuario"]
        password = values["senha"]
        tipoConta = verificarConta(user, password)
        if tipoConta == "VENDEDOR":
            janelaLogin.hide()
            janelaVendedor = telaVendedor(produtos, saldo_vendedor)
        elif tipoConta == "CLIENTE":
            janelaLogin.hide()
            janelaComprador = telaComprador(produtos, saldo)

    if window == janelaVendedor and event == "ADICIONAR PRODUTOS":
        janelaVendedor.hide()
        janelaAdicionarProduto = adicionarProduto()

    if window == janelaAdicionarProduto and event == "ADICIONAR":
        nome_produto = values["nome_produto"]
        valor_produto = values["valor_produto"]
        caminho_imagem = values["FILE"]

        if nome_produto and valor_produto and caminho_imagem:
            produtos.append([caminho_imagem, f"Valor: {valor_produto} R$"])
            sg.popup("Produto adicionado com sucesso!")
            janelaAdicionarProduto.hide()
            janelaVendedor.close()
            janelaVendedor = telaVendedor(produtos, saldo_vendedor)
        else:
            sg.popup("Por favor, preencha todos os campos.")

    if window == janelaAdicionarProduto and event == "CANCELAR":
        janelaAdicionarProduto.hide()
        janelaVendedor.un_hide()

    if window == janelaVendedor and event == "VOLTAR":
        janelaVendedor.hide()
        janelaMenu.un_hide()

    if window == janelaComprador and event == "VOLTAR":
        janelaComprador.hide()
        janelaMenu.un_hide()

    if window == janelaAdicionarProduto and event == "VOLTAR":
        janelaAdicionarProduto.hide()
        janelaVendedor.un_hide()

    if window == janelaSaldo and event == "VOLTAR":
        janelaSaldo.hide()
        janelaComprador.un_hide()

    if window == janelaComprador and event == "Adicionar saldo":
        janelaComprador.hide()
        janelaSaldo = adicionarSaldo()

    if window == janelaComprador and event == "Consultar saldo":
        sg.popup("Seu saldo é de " + str(saldo) + " R$")

    if window == janelaSaldo and event == "OK":
        saldo_inserido = values['saldo']
        try:
            saldo = float(saldo_inserido) + saldo
            janelaSaldo.close()
            janelaComprador = telaComprador(produtos, saldo)
            sg.popup("Seu saldo é de " + str(saldo) + "R$")
        except ValueError:
            sg.popup("Valor inserido inválido. Insira um número.")

    for indice, produto in enumerate(produtos):
        if window == janelaComprador and event == f"comprar_{indice}":
            realizarCompra(indice, produtos, saldo)
            if saldo >= valor_produto:

                saldo -= valor_produto
                saldo_vendedor += valor_produto


janelaMenu.close()
