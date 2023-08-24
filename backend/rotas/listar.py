from config import *
from classes.score import *


@app.route("/listar/<string:classe>")
def listar(classe):

    dados = None

    if classe == "Score":
        dados = db.session.query(Score).all()
        
    if dados:
        dados_json = []
        for d in dados:
            dados_json.append(d.json())

        resposta = {"resultado": "ok", "detalhes": dados_json}
        
    elif dados == []:
        resposta = jsonify({"resultado": "Erro!", "detalhes": "Sem dados"})
    
    else:
        resposta = jsonify({"resultado": "Erro!", "detalhes": "Classe informada inválida: "+classe})

    return resposta