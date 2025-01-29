from graphics import *
import csv
import os  # operating system
from datetime import datetime
import webbrowser

def carregar_estoque():
    estoque = []
    if not os.path.exists('estoque.csv'):  # verifica se o arquivo existe
        with open('estoque.csv', mode='w', newline='', encoding='utf-8') as arq:
            writer = csv.writer(arq)       # objeto escritor do modulo csv
            writer.writerow(['Código', 'Nome', 'Valor', 'Quantidade'])  # cria o cabeçalho se não existir
        return estoque  # retorna lista vazia se o arquivo foi recém-criado

    with open('estoque.csv', mode='r', encoding='utf-8') as arq:
        linhas = arq.readlines()  # le todas as linhas do arquivo
        for linha in linhas[1:]:  # pula o cabeçalho
            info = linha.strip().split(',')  # remove todos os caracteres em branco e vírgulas
            estoque.append(info)
    return estoque

def obter_proximo_codigo():
    estoque = carregar_estoque()
    if estoque:
        ultimo_codigo = int(estoque[-1][0])  # pega o código do último produto
        return ultimo_codigo + 1
    return 1  # se não houver produtos, começa em 1

def adicionar_estoque(nome, valor, quantidade):
    codigo = obter_proximo_codigo()
    with open('estoque.csv', mode='a', newline='', encoding='utf-8') as arq:    # usa o "a" quando se quer adicionar conteudo sem apagar o existente
        writer = csv.writer(arq)
        writer.writerow([codigo, nome, valor, quantidade])

def atualizar_estoque(estoque):
    with open('estoque.csv', mode='w', newline='', encoding='utf-8') as arq:    # "w" para sobrescrever o arquivo
        writer = csv.writer(arq)
        writer.writerow(['Código', 'Nome', 'Valor', 'Quantidade'])  # reescreve o cabeçalho
        writer.writerows(estoque)  # salva os dados do estoque atualizado

def registrar_compra(codigo, nome, quantidade):
    data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')  # formata a data e horario
    with open('historico.csv', mode='a', newline='', encoding='utf-8') as arq:
        writer = csv.writer(arq)
        writer.writerow([codigo, nome, quantidade, data_atual])  # salva a compra

def carregar_historico():
    historico = []
    if not os.path.exists('historico.csv'):
        with open('historico.csv', mode='w', newline='', encoding='utf-8') as arq:
            writer = csv.writer(arq)
            writer.writerow(['Código', 'Nome', 'Quantidade', 'Data'])  # cabeçalho do histórico
        return historico  # retorna uma lista vazia se o arquivo foi recém-criado

    with open('historico.csv', mode='r', encoding='utf-8') as arq:
        linhas = arq.readlines()
        for linha in linhas[1:]: 
            info = linha.strip().split(',')
            historico.append(info)
    return historico


def tela_inicial():
    win_inicial = GraphWin('Gestão de Estoque', 600, 500)  # cria a janela principal
    win_inicial.setBackground('black')  # define a cor do fundo

    logo = Image(Point(310, 130), 'logo-fb.png')  # coloca a imagem naquele ponto específico
    logo.draw(win_inicial)  # desenha na janela

    buttons = []
    buttons_left = ['Cadastrar Produto', 'Verificar Estoque', 'Realizar Compra']
    buttons_right = ['Busca no Estoque', 'Histórico de Compras', 'Gerar Relatório']  # nomes dos botões
    for i, text in enumerate(buttons_left):
        button = Rectangle(Point(70, 250 + i * 70), Point(270, 300 + i * 70))  # cria o botão e toda vez que o i aumenta consequentemente a posição y do próximo botão muda
        button.setOutline('white')  # define a cor do traço do botão
        button.draw(win_inicial)  # desenha o botão
        label = Text(button.getCenter(), text)  # escreve o nome do botão no centro do retângulo
        label.setTextColor('white')
        label.draw(win_inicial)
        buttons.append((button, text))

    for i, text in enumerate(buttons_right):
        button = Rectangle(Point(320, 250 + i * 70), Point(520, 300 + i * 70))  # cria o botão e toda vez que o i aumenta consequentemente a posição y do próximo botão muda
        button.setOutline('white')  # define a cor do traço do botão
        button.draw(win_inicial)  # desenha o botão
        label = Text(button.getCenter(), text)  # escreve o nome do botão no centro do retângulo
        label.setTextColor('white')
        label.draw(win_inicial)
        buttons.append((button, text))

    while True:    # loop infinito para aguardar os cliques
        click = win_inicial.checkMouse()     # coordenadas do mouse
        if click:
            for button, text in buttons:  # verifica se o clique está dentro dos limites do botão atual
                if button.getP1().getX() <= click.getX() <= button.getP2().getX() and button.getP1().getY() <= click.getY() <= button.getP2().getY():
                    if text == 'Cadastrar Produto':
                        cadastrar_produto()
                    elif text == 'Verificar Estoque':
                        verificar_estoque()
                    elif text == 'Realizar Compra':
                        realizar_compra()
                    elif text == 'Busca no Estoque':
                        busca_estoque()
                    elif text == 'Histórico de Compras':
                        mostrar_historico()
                    elif text == 'Gerar Relatório':
                        gerar_relatorio()

def sucesso(message):
    win_sucesso = GraphWin('Sucesso', 300, 150)
    win_sucesso.setBackground('black')

    text = Text(Point(150, 50), message)
    text.setTextColor('white')
    text.setStyle('bold')
    text.draw(win_sucesso)

    button = Rectangle(Point(100, 100), Point(200, 130))
    button.setFill('red')
    button.setOutline('red')
    button.draw(win_sucesso)

    label = Text(button.getCenter(), 'OK')
    label.setTextColor('white')
    label.setStyle('bold')
    label.draw(win_sucesso)

    while True:
        click = win_sucesso.getMouse()
        if button.p1.x <= click.getX() <= button.p2.x and button.p1.y <= click.getY() <= button.p2.y:
            break  # sai do loop quando clicar no botão

    win_sucesso.close()

def criar_botao_sair(win, tamanho):
    if tamanho == 400:
        button_sair = Rectangle(Point(350, 10), Point(390, 30))
    elif tamanho == 600:
        button_sair = Rectangle(Point(550, 10), Point(590, 30))
    elif tamanho == 800:
        button_sair = Rectangle(Point(740, 10), Point(780, 30))

    button_sair.setFill('gray')
    button_sair.setOutline('white')
    button_sair.draw(win)
    
    label_sair = Text(button_sair.getCenter(), 'X')
    label_sair.setTextColor('white')
    label_sair.draw(win)

    return button_sair


def cadastrar_produto():
    win_cadastro = GraphWin('Cadastro de Produtos', 400, 400) 
    win_cadastro.setBackground('black')

    labels = ['Nome:', 'Valor:', 'Quantidade:']
    entries = []                                            # lista para armazenar os inputs
    for i, text in enumerate(labels):
        label = Text(Point(100, 60 + i * 60), text)         # cria o label do input com posição fixa no eixo X (100), aumentando apenas o Y para acomodar os outros labels proporcionalmente
        label.setTextColor('white')
        label.setStyle('bold')
        label.draw(win_cadastro)
        
        entry = Entry(Point(250, 60 + i * 60), 15)          # cria o input ao lado do label, de tamanho 15
        entry.setTextColor('white')
        entry.draw(win_cadastro)
        entries.append(entry)

    button = Rectangle(Point(90, 300), Point(290, 340))
    button.setOutline('red')
    button.setFill('red')
    button.draw(win_cadastro)
    label = Text(button.getCenter(), 'Cadastrar')
    label.setTextColor('white')
    label.setStyle('bold')
    label.draw(win_cadastro)

    warning = Text(Point(200, 280), '')     # cria um texto inicialmente vazio para exibir mensagens de erro caso necessário
    warning.setTextColor('red')
    warning.draw(win_cadastro)

    button_sair = criar_botao_sair(win_cadastro, 400)

    while True:
        click = win_cadastro.getMouse()

        # verifica se clicou no botão "Sair"
        if button_sair.getP1().getX() <= click.getX() <= button_sair.getP2().getX() and button_sair.getP1().getY() <= click.getY() <= button_sair.getP2().getY():
            win_cadastro.close()
            break

        if 90 <= click.getX() <= 250 and 300 <= click.getY() <= 340:    # verifica se o clique ocorreu dentro do botão "Cadastrar"
            
            values = []
            for entry in entries:
                values.append(entry.getText())                           # loop para armazenar o texto dos inputs ja que os entries são objetos

            if not all(values):                                              # verifica se há algum campo vazio
                warning.setText('Preencha todos os campos.')  
            elif not values[1].isdigit() or not values[2].isdigit():   # valida os inputs 
                warning.setText('Valor e Quantidade devem ser numéricos.')   
            else:
                adicionar_estoque(values[0], values[1], values[2])     # salva o produto
                win_cadastro.close()
                sucesso('Item cadastrado com sucesso!')
                return                                                  # sai da função

def verificar_estoque():
    estoque = carregar_estoque()

    win_verificar = GraphWin('Estoque', 800, 800)
    win_verificar.setBackground('black')

    # adiciona o cabeçalho
    header = Text(Point(400, 35), 'Estoque Atual')
    header.setTextColor('white')
    header.setSize(16)
    header.draw(win_verificar)

    # desenha o header
    retangulo_header = Rectangle(Point(0, 100), Point(800, 60))
    retangulo_header.setOutline('red')
    retangulo_header.setFill('red')
    retangulo_header.draw(win_verificar)

    # conteúdo do header
    colunas = ['Código', 'Nome', 'Valor', 'Quantidade']
    posicoes_x = [75, 210, 360, 510]  # posições X das colunas
    for i, nome in enumerate(colunas):
        label = Text(Point(posicoes_x[i], 80), nome)
        label.setTextColor('white')
        label.setStyle('bold')
        label.draw(win_verificar)

    buttons = []   # lista para identificar qual botão foi clicado
    for i, row in enumerate(estoque):
        y_position = 140 + i * 45  # fefine a posição Y para as células e botões

        # cria e exibe cada célula de informação do estoque
        for j, value in enumerate(row):
            cell = Text(Point(posicoes_x[j], y_position), value)
            cell.setTextColor('white')
            cell.draw(win_verificar)

        # cria o botão "Repor"
        button_repor = Rectangle(Point(600, y_position - 15), Point(680, y_position + 15))
        button_repor.setFill('blue')
        button_repor.setOutline('blue')
        button_repor.draw(win_verificar)
        label_repor = Text(button_repor.getCenter(), 'Repor')
        label_repor.setTextColor('white')
        label_repor.setStyle('bold')
        label_repor.setSize(11)
        label_repor.draw(win_verificar)

        # cria o botão "Excluir"
        button_excluir = Rectangle(Point(700, y_position - 15), Point(780, y_position + 15))
        button_excluir.setFill('red')
        button_excluir.setOutline('red')
        button_excluir.draw(win_verificar)
        label_excluir = Text(button_excluir.getCenter(), 'Excluir')
        label_excluir.setTextColor('white')
        label_excluir.setStyle('bold')
        label_excluir.setSize(11)
        label_excluir.draw(win_verificar)

        buttons.append((button_repor, button_excluir, row[0]))  # código do produto

        button_sair = criar_botao_sair(win_verificar, 800)

    # loop para pegar os cliques nos botões
    while True:
        click = win_verificar.getMouse()

        # verifica se clicou no botão "Sair"
        if button_sair.getP1().getX() <= click.getX() <= button_sair.getP2().getX() and button_sair.getP1().getY() <= click.getY() <= button_sair.getP2().getY():
            win_verificar.close()
            break

        for button_repor, button_excluir, codigo in buttons:
            if button_repor.getP1().getX() <= click.getX() <= button_repor.getP2().getX() and button_repor.getP1().getY() <= click.getY() <= button_repor.getP2().getY():
                repor_estoque(codigo)  # chama a função de reposição
                win_verificar.close()
                verificar_estoque()  # atualiza a tela
                return

            elif button_excluir.getP1().getX() <= click.getX() <= button_excluir.getP2().getX() and button_excluir.getP1().getY() <= click.getY() <= button_excluir.getP2().getY():
                excluir_produto(codigo)  # chama a função de exclusão
                win_verificar.close()
                verificar_estoque()  # atualiza a tela
                return

def repor_estoque(codigo):
    estoque = carregar_estoque()
    
    for i, produto in enumerate(estoque):
        if produto[0] == codigo:                    # compara os códigos do estoque com o do que foi clicado
            nova_quantidade = int(produto[3]) + 10  # reabastece com +10 unidades
            estoque[i][3] = str(nova_quantidade)    

    atualizar_estoque(estoque)
    sucesso('Estoque reposto com sucesso!')

def excluir_produto(codigo):
    estoque = carregar_estoque()
    estoque_filtrado = []
    for produto in estoque:
        if produto[0] != codigo:  # se o código do produto for diferente do código a ser removido
            estoque_filtrado.append(produto)  # adiciona o produto na nova lista

    atualizar_estoque(estoque_filtrado)
    sucesso('Produto excluído com sucesso!')

def realizar_compra():
    estoque = carregar_estoque()

    win_compra = GraphWin('Realizar Compra', 800, 800)
    win_compra.setBackground('black')

    # adiciona o cabeçalho
    header = Text(Point(400, 40), 'Disponível para Compra')
    header.setTextColor('white')
    header.setSize(16)
    header.draw(win_compra)

    # desenha o header
    retangulo_header = Rectangle(Point(0, 120), Point(800, 70))
    retangulo_header.setOutline('red')
    retangulo_header.setFill('red')
    retangulo_header.draw(win_compra)

    # cabeçalho
    cod = Text(Point(75, 95), 'Código')
    cod.setTextColor('white')
    cod.setStyle('bold')
    cod.draw(win_compra)
    
    nome = Text(Point(210, 95), 'Nome')
    nome.setStyle('bold')
    nome.setTextColor('white')
    nome.draw(win_compra)
    
    valor = Text(Point(360, 95), 'Valor')
    valor.setStyle('bold')
    valor.setTextColor('white')
    valor.draw(win_compra)
    
    qtd = Text(Point(510, 95), 'Quantidade')
    qtd.setTextColor('white')
    qtd.setStyle('bold')
    qtd.draw(win_compra)

    button_sair = criar_botao_sair(win_compra, 800)

    buttons = []      # lista para identificar qual botão foi clicado
    for i, linha in enumerate(estoque):
        y_position = 140 + i * 45  # define a posição Y para as células e botões
        for j, value in enumerate(linha):     # escreve a info do estoque
            cell = Text(Point(70 + j * 150, y_position), value)
            cell.setTextColor('white')
            cell.draw(win_compra)
            
        if len(linha) > 0:     # garante que a linha tenha valores
            button = Rectangle(Point(650, y_position - 15), Point(750, y_position + 15))
            button.setFill('red')
            button.setOutline('red')
            button.draw(win_compra)
            
            label = Text(button.getCenter(), 'Comprar')
            label.setTextColor('white')
            label.setStyle('bold')
            label.draw(win_compra)
            
            buttons.append((button, linha[1], linha[3]))

    while True:
        click = win_compra.getMouse()
        # verifica se clicou no botão "Sair"
        if button_sair.getP1().getX() <= click.getX() <= button_sair.getP2().getX() and button_sair.getP1().getY() <= click.getY() <= button_sair.getP2().getY():
            win_compra.close()
            break

        for button, nome, quantidade in buttons:
            if button.getP1().getX() <= click.getX() <= button.getP2().getX() and button.getP1().getY() <= click.getY() <= button.getP2().getY():
                win_compra.close()
                comprar_item(nome, quantidade)
                return

def comprar_item(nome, quantidade):
    estoque = carregar_estoque() 

    win_item = GraphWin(f'Comprar {nome}', 400, 200)
    win_item.setBackground('black')

    text = Text(Point(200, 50), f'Deseja comprar quantas unidades de {nome}?\nQuantidade disponível: {quantidade}')
    text.setTextColor('white')
    text.draw(win_item)
    entry = Entry(Point(200, 100), 15)
    entry.draw(win_item)

    button = Rectangle(Point(100, 140), Point(300, 170))
    button.setFill('red')
    button.setOutline('red')
    button.draw(win_item)
    label = Text(button.getCenter(), 'Finalizar Compra')
    label.setTextColor('white')
    label.setStyle('bold')
    label.draw(win_item)

    warning = Text(Point(150, 130), '')
    warning.setTextColor('red')
    warning.draw(win_item)

    while True:
        click = win_item.getMouse()
        
        if 100 <= click.getX() <= 300 and 140 <= click.getY() <= 170:   # verifica se foi clicado o botão de finalizar compra
            quantidade_comprada = entry.getText()

            # verifica se o valor digitado é numérico e dentro do estoque disponível
            if quantidade_comprada.isdigit() and int(quantidade_comprada) <= int(quantidade):
                nova_quantidade = int(quantidade) - int(quantidade_comprada)

                # atualiza o estoque no arquivo
                for i, produto in enumerate(estoque):
                    if produto[1] == nome:  # compara o nome dos produtos com o que foi selecionado para compra
                        estoque[i][3] = str(nova_quantidade)  # atualiza a quantidade
                        codigo_produto = produto[0]  # pega o código do produto

                atualizar_estoque(estoque)  # salva o estoque atualizado
                registrar_compra(codigo_produto, nome, quantidade_comprada)

                win_item.close()
                sucesso('Compra realizada com sucesso!')
                return  # sai da função
            else:
                warning.setText('Quantidade disponível insuficiente.')

def busca_estoque():
    estoque = carregar_estoque() 

    win_busca = GraphWin('Buscar Produto', 600, 400)
    win_busca.setBackground('black')

    titulo = Text(Point(300, 50), 'Buscar Produto no Estoque')
    titulo.setTextColor('white')
    titulo.setSize(14)
    titulo.draw(win_busca)

    entry = Entry(Point(250, 100), 20)  # campo de entrada para o nome ou código do produto
    entry.draw(win_busca)

    button_buscar = Rectangle(Point(370, 85), Point(470, 115))
    button_buscar.setFill('red')
    button_buscar.setOutline('red')
    button_buscar.draw(win_busca)
    label_buscar = Text(button_buscar.getCenter(), 'Buscar')
    label_buscar.setTextColor('white')
    label_buscar.setStyle('bold')
    label_buscar.draw(win_busca)

    button_sair = criar_botao_sair(win_busca, 600)

    # exibe os resultados
    resultado_texto = Text(Point(300, 230), '')
    resultado_texto.setTextColor('white')
    resultado_texto.setSize(12)
    resultado_texto.draw(win_busca)

    while True:
        click = win_busca.getMouse()  # aguarda o clique do usuário

        if button_buscar.getP1().getX() <= click.getX() <= button_buscar.getP2().getX() and button_buscar.getP1().getY() <= click.getY() <= button_buscar.getP2().getY():
            termo_busca = entry.getText().strip().lower()  # obtem o codigo ou nome do produto
            resultados = []

            for produto in estoque:
                if termo_busca in produto[1].lower() or produto[0] == termo_busca:  # verifica pelo nome ou código
                    resultados.append(f'Código: {produto[0]}, Nome: {produto[1]}, Quantidade: {produto[3]}')

            # atualiza o texto do resultado
            if resultados:
                resultado_texto.setText('\n'.join(resultados))
            else:
                resultado_texto.setText('Nenhum produto encontrado.')

        elif button_sair.getP1().getX() <= click.getX() <= button_sair.getP2().getX() and button_sair.getP1().getY() <= click.getY() <= button_sair.getP2().getY():
            win_busca.close()
            return  # fecha a janela e sai da função


def mostrar_historico():
    historico = carregar_historico()

    win_historico = GraphWin('Histórico de Compras', 800, 800)
    win_historico.setBackground('black')

    # adiciona o cabeçalho
    header = Text(Point(400, 35), 'Histórico de Compras')
    header.setTextColor('white')
    header.setSize(16)
    header.draw(win_historico)

    # desenha o header
    retangulo_header = Rectangle(Point(0, 100), Point(800, 60))
    retangulo_header.setOutline('red')
    retangulo_header.setFill('red')
    retangulo_header.draw(win_historico)

    # conteúdo do header
    colunas = ['Código', 'Nome', 'Quantidade', 'Data']
    posicoes_x = [100, 250, 450, 650]  # posições X das colunas
    for i, nome in enumerate(colunas):
        label = Text(Point(posicoes_x[i], 80), nome)
        label.setTextColor('white')
        label.setStyle('bold')
        label.draw(win_historico)

    # exibe as compras do histórico
    for i, linha in enumerate(historico):
        for j, value in enumerate(linha):
            cell = Text(Point(posicoes_x[j], 120 + i * 45), value)
            cell.setTextColor('white')
            cell.draw(win_historico)

    button_sair = criar_botao_sair(win_historico, 800)

    # loop de interação para verificar cliques
    while True:
        click = win_historico.getMouse()

        # verifica se clicou no botão "Sair"
        if button_sair.getP1().getX() <= click.getX() <= button_sair.getP2().getX() and button_sair.getP1().getY() <= click.getY() <= button_sair.getP2().getY():
            win_historico.close()
            break

def gerar_relatorio():
    estoque = carregar_estoque()
    historico = carregar_historico()

    html_content = '''
    <html>
    <head>
        <title>Relatório de Estoque e Compras</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { text-align: center; color: #333; }
            table { width: 100%; border-collapse: collapse; margin: 20px 0; }
            th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
            th { background: #ff5733; color: white; }
        </style>
    </head>
    <body>
        <h1>Relatório de Estoque</h1>
        <table>
            <tr>
                <th>Código</th>
                <th>Nome</th>
                <th>Valor</th>
                <th>Quantidade</th>
            </tr>'''
    
    # adiciona os produtos do estoque a tabela
    for produto in estoque:
        html_content += f'''
            <tr>
                <td>{produto[0]}</td>
                <td>{produto[1]}</td>
                <td>R$ {produto[2]}</td>
                <td>{produto[3]}</td>
            </tr>'''
    
    html_content += '''
        </table>

        <h1>Histórico de Compras</h1>
        <table>
            <tr>
                <th>Código</th>
                <th>Nome</th>
                <th>Quantidade Comprada</th>
                <th>Data</th>
            </tr>'''

    # adiciona o histórico de compras a tabela
    for compra in historico:
        html_content += f'''
            <tr>
                <td>{compra[0]}</td>
                <td>{compra[1]}</td>
                <td>{compra[2]}</td>
                <td>{compra[3]}</td>
            </tr>'''

    html_content += '''
        </table>
    </body>
    </html>'''

    with open('relatorio.html', 'w', encoding='utf-8') as file:  # salva o HTML no arquivo
        file.write(html_content)

    webbrowser.open('relatorio.html')                            # abre o arquivo HTML no navegador automaticamente

    sucesso('Relatório gerado com sucesso!')

tela_inicial()