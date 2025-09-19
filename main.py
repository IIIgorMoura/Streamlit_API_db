# SQL_ALCHEMY
    # é o que permite a conexão da API com o BD
    # pip install flask_sqlalchemy

# FLASK - permite a criação de API com Python

# Response e Request -> Requisição
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask('carros')


# SQL_ALCHEMY cria e modifica td no DB
    # por isso vamos adicionar 'tracking' e revisão de alterações
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# URI] = 'siteDB://user:senha' // '%40' é o '@', pq o char @ é usado como declarador do IP
# 1: User - 2: Senha - 3: 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Senai%40134@127.0.0.1/db_carro'



# nome pode ser diferente
mybd = SQLAlchemy(app)

# Classe para definir modelo dos dados que correspondem a tabela do db
    # Em POO, class é o padrão/estrutura/template a ser seguido
    # Em POO, o objeto são os registros, os valores que serão criados, usando o class como molde
class Carros(mybd.Model):
    __tablename__ = 'tb_carro'
    id_carro = mybd.Column(mybd.Integer, primary_key=True)
    marca = mybd.Column(mybd.String(255))
    modelo = mybd.Column(mybd.String(255))
    ano = mybd.Column(mybd.String(255))
    cor = mybd.Column(mybd.String(255))
    valor = mybd.Column(mybd.String(255))
    numero_vendas = mybd.Column(mybd.String(255))

    # converter o objeto do carro em json, pois originalmente é em colunas
    def to_json(self):
        return {
            # o primeiro 'id_carro' tem que ser igual ao q está no DB, o do self é a variável previamente usada no programa
            "id_carro": self.id_carro,
            "marca": self.marca,
            "modelo": self.modelo,
            "ano": self.ano,
            "valor": float(self.valor),
            "numero_vendas": self.numero_vendas
        }
    


# --------------------------------------------

# Method 1 - GET
@app.route('/carros', methods=['GET'])
def seleciona_carro():
    # var para armazenar o que recebemos da API
        # retorna tudo na estrutura de colunas
    carro_selecionado = Carros.query.all()

        # por isso precisa ser convertido   
    carro_json = [
        # esse 'to_json' é a função que definimos dentro da classe previamente
        carro.to_json()
        for carro in carro_selecionado           
    ]

    # não precisa do make_response
        # status, 'nome do conteúdo', 'conteudo'
    return gera_resposta(200, "carros", carro_json)



# --------------------------------------------
# Method 2 - GET (POR ID)
@app.route('/carros/<int:id_carro_p>', methods=['GET'])
def seleciona_carro_id(id_carro_p):
    carro_selecionado = Carros.query.filter_by(id_carro=int(id_carro_p)).first()
    carro_json = carro_selecionado.to_json()
    return gera_resposta(200, carro_json, 'Carro encontrado!')




# Respostas padrão
    # status (http) 200 = deu certo; 
    # nome do conteúdo
    # conteudo
    # mensagem (opcional)

def gera_resposta(status, conteudo, mensagem=False):
    body = {}
    body['Lista de Carros'] = conteudo
    if (mensagem):
        body['mensagem'] = mensagem

    return Response(json.dumps(body), status=status, mimetype='application/json')
# Dumps - Converte o Dict (body) em Json(json.dumps)



# ---------------------------------------------
# Method 3 - POST
@app.route('/carros', methods=['POST'])
def criar_carro():
    requisicao = request.get_json()

    try:
        carro = Carros(
            id_carro = requisicao['id_carro'],
            marca = requisicao['marca'],
            modelo = requisicao['modelo'],
            ano = requisicao['ano'],
            valor = requisicao['valor'],
            cor = requisicao['cor'],
            numero_vendas = requisicao['numero_vendas']
        )

        
        # semelhante ao Commit manual no SQL
        mybd.session.add(carro)
        # enviar 'commitar' ao banco
        mybd.session.commit()

        return gera_resposta(201, carro.to_json(), 'Criado com sucesso')
    
    except Exception as e:
        print('Erro ao tentar postar: ', e)
        return gera_resposta(400, {}, 'Erro ao cadastrar!')
        


# --------------------------------------------
# Method 4 - DELETE
    # alguns dão erro por ter/ser chave estrangeira
@app.route('/carros/<id_carro_p>', methods=['DELETE'])
def deleta_carro(id_carro_p):
    carro = Carros.query.filter_by(id_carro = id_carro_p).first()

    try:
        mybd.session.delete(carro)
        mybd.session.commit()
        return gera_resposta(200, carro.to_json(), "Deletado com sucesso!")
    except Exception as e:
        print('Erro ao tentar deletar:', e)
        return gera_resposta(400, {}, "Erro ao deletar!")



# --------------------------------------------
# Method 5 - PUT
@app.route('/carros/<id_carro_p>', methods=['PUT'])
def atualiza_carro(id_carro_p):
    carro = Carros.query.filter_by(id_carro = id_carro_p).first()
    requisicao = request.get_json()

    try:
        if ('marca' in requisicao):
            carro.marca = requisicao['marca']
        if ('modelo' in requisicao):
            carro.modelo = requisicao['modelo']
        if ('ano' in requisicao):
            carro.ano = requisicao['ano']
        if ('valor' in requisicao):
            carro.valor = requisicao['valor']
        if ('cor' in requisicao):
            carro.cor = requisicao['cor']
        if ('numero_vendas' in requisicao):
            carro.numero_vendas = requisicao['numero_vendas']

        mybd.session.add(carro)
        mybd.session.commit()

        return gera_resposta(200, carro.to_json(), "Atualizado")
    except Exception as e:
        print("Erro ao tentar atualizar: ", e)



# --------------------------------------------
# execução
    # debug é para não bloquear, pois sem ele acha que está no modo produção
app.run(port=5000, host='localhost', debug=True)