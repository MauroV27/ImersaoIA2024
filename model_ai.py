from dotenv import load_dotenv
load_dotenv()

import os
import json
import pandas as pd
import google.generativeai as genai

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
  "candidate_count": 1,
  "temperature": 0.1, # Pelo modelo se comportar como uma API, optou-se por usar
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name='gemini-1.0-pro',
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)


examples = pd.DataFrame([
    {
        "target_midia" : "Manga",
        "reference" : "Oppenheimer (Filme)",
        "num_resp" : 2,
        "resultado" : [{
            "titulo": "Pluton",
            "autor": "Naoki Urasawa",
            "genero": "Drama, Ficção Científica, História",
            "sinopse": "Um jovem cientista alemão se junta ao projeto Manhattan para desenvolver a bomba atômica durante a Segunda Guerra Mundial.",
          },
          {
            "titulo": "This is How I Kill Your King",
            "autor": "Warren Ellis e Giannis Milonogiannis",
            "genero": "Drama, Ficção Científica, Thriller",
            "sinopse": "Um agente do governo americano investiga uma série de assassinatos que podem estar relacionados ao desenvolvimento da bomba atômica.",
          }]
    }, {
        "target_midia" : "Serie",
        "reference" : "O show de truman (Filme)",
        "num_resp" : 2,
        "resultado" : [{
            "titulo": "Black Mirror",
            "ano": "2011-2019",
            "genero": "Ficção Científica, Drama",
            "sinopse": "Uma série de antologia que explora o lado obscuro da tecnologia e seus impactos na sociedade.",
          },
          {
            "titulo": "Westworld",
            "ano": "2016-presente",
            "genero": "Ficção Científica, Drama",
            "sinopse": "Um parque temático futurista onde androides vivem em um mundo do Velho Oeste, mas as coisas começam a dar errado.",
          }]
    }, {
        "target_midia" : "Filme",
        "reference" : "Blame! (manga)",
        "num_resp" : 4,
        "resultado" : [{
            "titulo": "Ghost in the Shell",
            "ano": "1995",
            "genero": "Ação, Ficção Científica",
            "sinopse": "Um cyborg policial investiga um hacker que está implantando memórias falsas em pessoas."
          },
          {
            "titulo": "O Gigante de Ferro",
            "ano": "1999",
            "genero": "Animação, Aventura",
            "sinopse": "Um menino faz amizade com um robô gigante que é caçado pelo governo."
          },
          {
            "titulo": "Akira",
            "ano": "1988",
            "genero": "Animação, Ação",
            "sinopse": "Em uma Tóquio distópica, um jovem motociclista se envolve em uma conspiração governamental."
          },
          {
            "titulo": "Blade Runner 2049",
            "ano": "2017",
            "genero": "Ficção Científica, Thriller",
            "sinopse": "Um policial replicante investiga o mistério de uma criança nascida de uma mãe humana."
          }]
    }, {
        "target_midia" : "Filme",
        "reference" : "icjqicjpjcpj",
        "num_resp" : 2,
        "resultado" : {"error": "O elemento de referência não foi reconhecido, por favor tente novamente."},
    }, {
        "target_midia" : "",
        "reference" : "O lobo de Wallstreet",
        "num_resp" : 2,
        "resultado" : {"error": "Necessário passar um tipo de mídia valida como target, por favor tente novamente."},
    }
])

def process_data(media_type, reference):
    send_query_to_search = f"""
        Tendo como base os exemplos : {examples}, responda como se fosse uma API em JSON para o seguinte caso :

        target_midia : {media_type},
        reference : {reference},
        num_resp : 5,

        resultado :
    """

    response = model.generate_content(send_query_to_search)
    model_resp = response.text

    #print(model_resp)

    filter_resp = model_resp.replace("```", "").replace("json", "")
    filter_resp = json.loads(filter_resp)

    #print(filter_resp)

    return filter_resp["resultado"]

