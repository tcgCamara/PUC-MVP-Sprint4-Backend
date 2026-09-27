from flask_openapi3 import OpenAPI, Tag
from flask import redirect, request
from flask_cors import CORS
from sqlalchemy import func, delete
import requests

from model import Session, Lista, Usuarios
from schemas import *

app = OpenAPI(__name__)
CORS(app)

#Construindo as tags para apresentação no swagger
tag_usuario = Tag(name="Usuários/Login", description="Cadastro e login de usuário no sistema.")
tag_apresentação = Tag(name="Swagging", description="Apresentação em Swagger das funções da API para comunicação com front-end.")
tag_lista = Tag(name="Lista de Cartas", description="Inclusão, consulta e exclusão das cartas na lista.")
tag_buscacep = Tag(name="Busca de CEP", description="Busca as informações do endereço a partir do CEP.")

@app.get('/', tags=[tag_apresentação])
def swagging():
    """Apresenta todos os caminhos e funções para comunicação com a API

    Redirecionamento para /openapi, com a documentação Swagger, facilitando a visualização para utilização da API.
    """
    return redirect('/openapi')

# -----------------------------------------------------
# USUARIOS
# ----------------------------------------------------

@app.post('/usuario', tags=[tag_usuario],
          responses={"200": CadastroUsuario, "400": ErroSchema, "500": ErroSchema})
def cadastro_usuario (body: CadastroUsuario):
    """Rota para cadastrar usuários no banco de dados.

    Retorna o nome do usuário, cpf e e-mail cadastrados.
    """
    print(f'nome: {body.nome}, cpf: {body.cpf}, email: {body.email}.')
    
    # PARA O FUTURO, inserir validação da qualidade dos dados inseridos (cpf e e-amil)
    # Apesar de ser feito pelo front, vale reforçar caso seja feito entre serviços no back

    #VERIFICAR se contém outro usuário com mesmo nome
    try:
        session = Session()
        nomeDaQuery = session.query(Usuarios).filter(Usuarios.nome == body.nome).first()

        if nomeDaQuery:
            erro = "Usuário já cadastrado. Tente outro login."
            return {"Mensagem": erro}, 400
        
        # UMA VEZ VALIDADO, o usuário não existindo no banco, o cadastro é realizado 
        insert_usuario = Usuarios(
            nome = body.nome,
            cpf = body.cpf,
            email = body.email
            )

        session.add(insert_usuario)
        session.commit()

        return estrutura_usuario(insert_usuario), 201

    except Exception as e:
        session.rollback()
        return {'Error': str(e)}, 500
    
    finally:
        session.close()

@app.get('/usuario', tags=[tag_usuario],
         responses={"200": LoginUsuario,"400": ErroSchema, "500": ErroSchema})
def login_usuario (query: LoginUsuario):
    """Realiza o login do usuário.
    
    A aplicação busca no banco se existe o usuário cadastrado. Caso não tenha, ele retorna a informação negativa.
    Apesar de serem realizados pelo método POST, este login é apenas valida a existência neste MVP.
    
    Retorna o nome do usuário cadastrado - quando tem sucesso."""

    userLogin = query.nome
    print(f'Tentativa de login com usuário -> {userLogin}')

    try:
        # PREPARANDO a sessão para realizar a consulta ao banco de dados.
        session = Session()
        usuarioValido = session.query(Usuarios).filter(Usuarios.nome == userLogin).first()

        # VERIFICA se o banco de dados retornou o usuário correspondente
        # ou se o retorno foi vazio, ou seja, o usuário não correspondia a um usuário
        # cadastrado no banco de dados
        if not usuarioValido:
            erro = "Usuário não encontrado."
            return {"Mensagem": erro}, 400
        
        return {'nome': usuarioValido.nome}, 200

    except Exception as e:
        session.rollback()
        return {"Mensagem": e}, 500
    
    finally:
        session.close()


#-----------------------------------------------------
# REGISTRO E CONSULTA DE CARTAS
#-----------------------------------------------------

@app.get('/cartas', tags=[tag_lista])
def retorna_cartas_usuario (query: LoginUsuario):
    """Busca as cartas na lista de impressão do usuário. 
    
    Retorna uma estrutura de todas as cartas cadastradas na lista do usuário logado
    """
    print(query.nome)
    usuarioLogado = query.nome


    try: 
        session = Session()
        
        # VALIDANDO o usuário que solicita os dados
        usuarioId = session.query(Usuarios).filter(Usuarios.nome == usuarioLogado).first()
        if not usuarioId:
            return {"Mensagem": "Problema ao validar o usuário."}, 400
        
        usuarioIdNumero = usuarioId.id

        listaCartasCadastradas = session.query(Lista.carta, func.sum(Lista.quantidade)).filter(Lista.usuario_id == usuarioIdNumero).group_by(Lista.carta).all()

        respostaDeCartas = []
    
        for carta, total in listaCartasCadastradas:
            respostaDeCartas.append({
                "carta": carta,
                "quantidade": total
            })

        return {'lista': respostaDeCartas}, 200
    
    except Exception as e:
        return {"mensagem": str(e)}, 500
    
    finally:
        session.close()

@app.post('/carta', tags=[tag_lista],
          responses={"201": AdicionarListaSchema, "400": ErroSchema, "500": ErroSchema})
def adiona_carta (body: AdicionarListaSchema):
    """Adiciona a carta a sua lista no banco de dados
    
    Retorna a confimação com o produto cadastrado na lista do usuário.
    """
    usuarioLogado = body.usuario
    cartaInserida = body.carta
    quantidadeCarta = body.quantidade

    try:
        session = Session()
        
        # VALIDANDO o usuário para pegar o ID dele
        usuarioValido = session.query(Usuarios).filter(Usuarios.nome == usuarioLogado).first()

        if not usuarioValido:
            msg = 'Usuário inexistente para cadastro.'
            return {'Mensagem': msg}, 400
        
        if quantidadeCarta <= 0:
            msg = 'Insira uma quantidade válida.'
            return {'Mensagem': msg}, 400

        carta_inserida = Lista(
                usuario_id = usuarioValido.id,
                carta = cartaInserida,
                quantidade = quantidadeCarta
            )

        session.add(carta_inserida)
        session.commit()
        
        return estrutura_lista(carta_inserida, usuarioLogado), 201

    except Exception as e:
        return {"Mensagem": str(e)}, 500
    
    finally:
        session.close()


#-----------------------------------------------------
# APAGA Informações do banco de dados
#-----------------------------------------------------

@app.delete('/cartas', tags=[tag_lista])
def deleta_carta (body: DeletarCartasSchema):
    """Deleta todas as cartas de nome selecionado da lista do usuario logado

    Retorna a confirmação da quantidade e nome da carta deletada com sucesso da lista.
    """

    usuarioLogado = body.usuario
    cartaParaDeletar = body.carta

    print(usuarioLogado)
    print(cartaParaDeletar)

    try:
        session = Session()

        # VALIDANDO o usuario
        usuarioValido = session.query(Usuarios).where(Usuarios.nome == usuarioLogado).first()
        if not usuarioValido:
            return {'mensagem': 'Usuário não encontrado.'}, 400

        print(usuarioValido.id)

        # VALIDANDO se a carta existe na lista do usuário
        usuarioValidoId = usuarioValido.id
        cartaValidada = session.query(Lista.carta).where(Lista.usuario_id == usuarioValidoId).where(Lista.carta == cartaParaDeletar).all()

        if not cartaValidada:
            return {'Mensagem': "Carta não encontrada na lista do usuário."}, 400

        listaParaDeletar = delete(Lista).where(Lista.usuario_id == usuarioValido.id, Lista.carta == cartaParaDeletar)
        
        session.execute(listaParaDeletar)
        session.commit()

        msg = f'As suas cartas de [{cartaParaDeletar}] foram excluídas de sua lista de impressão.'
        return {'mensagem': msg}, 200 
 
    except Exception as e:
        session.rollback()
        return {'mensagem': str(e)}, 500
 
    finally:
        session.close()

@app.delete('/cartasdousuario', tags=[tag_lista])
def deleta_todas_as_cartas (query: DeletarTodasAsCartasDoUsuario):

    usuarioLogado = query.usuario
    print(f'Nome do usuario recebido. -> {usuarioLogado}')

    try:
        session = Session()
        print('Banco de dados aberto...')

        # VALIDANDO o usuario
        usuarioValido = session.query(Usuarios).where(Usuarios.nome == usuarioLogado).first()
        if not usuarioValido:
            return {'mensagem': 'Usuário não encontrado.'}, 400
        print(f'Usuário validado com sucesso! -> {usuarioValido.id}: {usuarioValido}')

        listaDoDoUsuarioParaDeletar = delete(Lista).where(Lista.usuario_id == usuarioValido.id)
        print('Lista preparada para ser deletada.')

        session.execute(listaDoDoUsuarioParaDeletar)
        print('A ser deletada em 3... 2... 1...')

        session.commit()
        print('DELETADAS!')

        msg = f'As cartas de [{usuarioValido.id}] foram DELETADAS de lista do usuário.'
        print(msg)

        return {'mensagem': 'Lista de cartas deletada com sucesso'}, 204 
 
    except Exception as e:
        session.rollback()
        return {'mensagem': str(e)}, 500
 
    finally:
        session.close()

#-----------------------------------------------------
# CONECTAR a API de busca por CEP
#-----------------------------------------------------

@app.get('/buscacep', tags=[tag_buscacep],
         responses={"200": RetornoCepDoCliente, "400": ErroSchema})
def busca_cep (query: CodigoPostalFormato):
    """Conecta este backend à um serviço de API online onde busca informações de 
     determinado endereço a partir do número de CEP

    As informações buscadas servirão para o preenchimento automático do envio da lista de produtos.
    """
    #Pegar informações vindo da URL / 
    codigoPostal = query.cep 
    print('O CEP a ser buscado é: ' + codigoPostal)

    # VALIDAR o CEP recebido
    if len(codigoPostal) != 8 or not codigoPostal.isdigit():
        messageError = 'Código Postal (CEP) inválido'
        return {'mensagem': messageError}, 400

    print(f'o CEP {codigoPostal} verificado... e validado! ')

    # CONSTRUIR a URL para busca
    urlDaApi = f'http://viacep.com.br/ws/{codigoPostal}/json/'
    print (urlDaApi)


    # INICIAR o acesso da API externa
    try:
        dadosBrutoDoCep = requests.get(urlDaApi)
        print('FETCH finalizado com sucesso? Veremos...')

        if dadosBrutoDoCep.status_code != 200:
            print('API consultada com sucesso.')
            messageError = f"Problema ao validar CEP {codigoPostal}."
            return {"mensagem": messageError}, 400
            
        dadosJsonDoCep = dadosBrutoDoCep.json()
        print(dadosJsonDoCep)

        # TRATAR somente com os dados necessários para retornar ao cliente
        codigoPostalEstruturado = estrutura_cep(dadosJsonDoCep)

        return codigoPostalEstruturado, 200
        
    except Exception as e:
        print(f'DEU RUIM! Conserta isso daí. Código: {e}')
        return {'mensagem': str(e)}, 500
    # finally:
    #     registra_cep()

