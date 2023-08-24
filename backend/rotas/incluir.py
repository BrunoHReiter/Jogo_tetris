from config import *
from classes.score import *

@app.route("/incluir/<string:classe>", methods=["post"])
def incluir(classe):
    dados = request.get_json()

    try:
        nova = None
        if classe == "Score":
            nova = Score(**dados)

        db.session.add(nova)
        db.session.commit()
        resposta = jsonify({"resultado": "Pontos adicionado!"})

    except Exception as error:
        resposta = jsonify({"resultado": "Erro!", "detalhes": str(error)})

    return resposta