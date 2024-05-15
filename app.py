from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:marcela4463@db/loja'
db = SQLAlchemy(app)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    idade = db.Column(db.Integer)

    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

@app.route('/')
def criando():
    data = request.get_json()
    nome = data['nome']
    idade = data['idade']
    novoCliente = Cliente(nome, idade)
    db.session.add(novoCliente)
    db.session.commit()
    return jsonify({'mensagem': 'Cliente adicionado com sucesso!'})


@app.route('/Clientes', methods=['GET'])
def procurando():
    clientes = Cliente.query.all()
    listaClientes = []
    for C in clientes:
        listaClientes.append({'id': C.id, 'nome': C.nome, 'idade': C.idade})
    return jsonify({'Clientes queridos': listaClientes})

@app.route('/Clientes/<int:id>', methods=['GET'])
def procurandoPorID(id):
    cliente = Cliente.query.get(id)
    if cliente:
        return jsonify({'id': cliente.id, 'nome': cliente.nome, 'idade': cliente.idade})
    else:
        return jsonify({'mensagem': 'Não te encontramos! :('}), 404

@app.route('/AttCliente/<int:id>', methods=['PUT'])
def atualizando(id):
    cliente = Cliente.query.get(id)
    if cliente:
        data = request.get_json()
        cliente.nome = data['nome']
        cliente.idade = data['idade']
        db.session.commit()
        return jsonify({'mensagem': 'Sua conta foi atualizada com sucesso!'})
    else:
        return jsonify({'mensagem': 'Não te encontramos! :('}), 404
    
@app.route('/DeleteCliente/<int:id>', methods=['DELETE'])
def deletando(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return jsonify({'mensagem': 'Sua conta foi deletada! até mais ;)'})
    else:
        return jsonify({'mensagem': 'Não te encontramos! :('}), 404

if __name__ == '__main__':
    app.run(debug=True)