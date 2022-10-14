from flask import Flask, request, render_template
from pymongo import MongoClient
client = MongoClient("mongodb://192.168.100.148:27100")

print(client)

database = client.produtos

collection = database.produtos

app = Flask("Estoque")



add_produto = []

@app.route("/estoque", methods=["GET"]) #mostrando database
def dados():
    try:
        oi = []
        oi.pop()
    except:
        for i in collection.find():
            oi.append(i)
    return oi


@app.route("/cadastrar/produto", methods= ["POST"])
def addproduto():

    body = request.get_json()

    print(body)

    if("_id" not in body):
        return geraResponse(400, "O parametro _id é obrigatorio")
    
    if("Produto" not in body):
        return geraResponse(400, "O parametro produto é obrigatorio")

    if("categoria" not in body):
        return geraResponse(400, "O parametro categoria é obrigatorio")

    add_produto.append(body)
    collection.insert_many(add_produto)
    add_produto.pop()
    return geraResponse(200, "Produto adicionado")



@app.route("/remover/produto/<id>", methods=["DELETE"]) #deletar produto
def delete_user(id):
    collection.delete_one({"_id": id})
    return "Produto deletado do estoque"

@app.route("/estoque/<id>", methods=["POST"]) #alterando categoria(update)
def gupdate(id):
    cat = input("Digite a categoria:")
    collection.update_one({"_id": id}, {"$set": {"categoria": cat}})
    return "Dados modificados!"


def geraResponse(status, mensagem, nome_do_conteudo=False, conteudo=False):
    response = {}
    response["status"] = status
    response["mensagem"] = mensagem

    if(nome_do_conteudo and conteudo):
        response[nome_do_conteudo] = conteudo
    
    return response

if __name__ == '__main__':
  app.run(host = '0.0.0.0', debug=True, port='1010') 
