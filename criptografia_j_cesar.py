import requests
import json
import string
import hashlib

def busca_dados(token):
    #Faz o resquest das informações
    r = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token={}'.format(token))
    print(r.text)
    #gera_arquivo = json.loads(r.content)
    return r

def cria_arquivo(gera_arquivo):
    with open('answer.json', 'w') as f:
       json.dump(gera_arquivo, f)
    f.close()

def decodifica(gera_arquivo):
    #Definindo numero de casas e a frase cifrada
    numero_casas = gera_arquivo['numero_casas']
    cifrado = gera_arquivo['cifrado']
  
    #Gera o alfabeto
    alfabeto = list(string.ascii_lowercase)

    #Logica para descobrir a frase
    m = ''
    for c in cifrado:
           if c in alfabeto:
               c_index = alfabeto.index(c)
               #index - numero de casas % tamanho do alfabeto -> o resto é sempre a posição da letra no alfabeto
               m += alfabeto[(c_index - numero_casas)  % len(alfabeto)]
           else:
               m += c
    return m

def resumo_criptografico(decod):
    resumo = hashlib.sha1()
    resumo.update(decod.encode())
    resumo = resumo.hexdigest()

    return resumo

def atualiza_arquivo(decoficado,resumo):
    with open('answer.json', 'r+') as f:
            data = json.load(f)
            data['decifrado'] = decoficado
            data['resumo_criptografico'] = resumo
            f.seek(0)
            json.dump(data, f)
            f.truncate()
    f.close()


def envia_arquivo(token):
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token={}'.format(token)
    answer = {'answer': open('answer.json', 'rb')}
    submit = requests.post(url, files=answer)
    return submit

if __name__ == "__main__":
    token = ''
    r = busca_dados(token)
    arquivo = json.loads(r.content)
    cria_arquivo(arquivo)
    decodificado = decodifica(arquivo)
    resumo = resumo_criptografico(decodificado)
    atualiza_arquivo(decodificado,resumo)
    resposta = envia_arquivo(token) 
    print(resposta.text)


