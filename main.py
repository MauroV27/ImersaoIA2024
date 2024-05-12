from flask import Flask, render_template, request, jsonify
from model_ai import process_data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/enviarDados", methods=["POST"])
def enviar_dados():

    # print("dados request: ", request)
    # print("dados request: ", request.json)
    # print("dados request: ", request.data)
    # print("-> ", request.form)

    # for key, value in request.form.items():
    #     print(" --->> ", key, value)

    media = request.json["media"]
    ref = request.json["ref"]

    print("Entrada : ", media, ref)
    result = process_data(media_type=media, reference=ref)

    # Processe os dados recebidos (nome e email)
    print(result)

    resposta = {
        "mensagem": result
    }

    return jsonify(resposta)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')