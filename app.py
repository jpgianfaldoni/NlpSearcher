# app.py
# Required Imports
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import random
import json 
import sqlite3
from Levenshtein import distance as levenshtein_distance
import itertools
from itertools import islice


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))

#Função que itera sobre as palavras da search string e retorna uma lista de listas,
#onde cada lista é uma lista de tuplas no formato (id da palavra, tfidf, id do documento),
#ordenadas por Tfidf (Em resumo uma lista de listas invertidas)
def getTfidfLists(search_string):
    conn = sqlite3.connect('SQL.db')
    cursor = conn.cursor()
    doc_list = []
    lev_dist = 0
    min_lev_dist = 1000
    cursor.execute("SELECT word FROM words")
    m = cursor.fetchall()
    for w in search_string.split(" "):
        cursor.execute(f"SELECT word_id FROM words WHERE word ='{w}'")
        s = cursor.fetchall()
        if len(s) > 0:
            word_id = s[0][0]
            cursor.execute(f"SELECT word_id, tfidf, website_id FROM website_has_word WHERE word_id = '{word_id}' ORDER BY tfidf DESC")
            r = cursor.fetchall()
            doc_list.append(r[0:10]) 
        else:
            #Caso a palavra não seja encontrada no DB, encontra a palavra que possui a menor Levenshtein distance 
            for word in m:
                lev_dist = levenshtein_distance(w, word[0])
                if lev_dist < min_lev_dist:
                    min_lev_dist = lev_dist
                    sub_word = word[0]
            cursor.execute(f"SELECT word_id FROM words WHERE word ='{sub_word}'")
            s2 = cursor.fetchall()
            word_id2 = s2[0][0]
            cursor.execute(f"SELECT word_id, tfidf, website_id FROM website_has_word WHERE word_id = '{word_id2}' ORDER BY tfidf DESC")
            r2 = cursor.fetchall()
            doc_list.append(r2[0:10]) 
    return doc_list


#Função que recebe a saída da função getTfidfLists() e retorna um dicionário com os 
#10 sites que possuem a maior soma de Tfidfs
def getBestWebsites(doc_list):
    full_dict = {}
    scores_dict = {}
    final_result = {}
    for doc in doc_list:
        for word in doc:
            if word[2] in scores_dict:
                scores_dict[word[2]] += word[1]
            else:
                scores_dict[word[2]] = word[1]
        full_dict[word[0]] = scores_dict
        scores_dict = {}
    for k,v in full_dict.items():
        for k2,v2 in v.items():
            if k2 in final_result:
                final_result[k2] += v2
            else:
                final_result[k2] = v2
    sorted_dict = dict(sorted(final_result.items(),reverse=True, key=lambda item: item[1]))
    top_10 = take(10, sorted_dict.items())
    return list(zip(*top_10))[0]



#Função que recebe a saída da função getBestWebsites e retorna as informações
#título, url e conteúdo da página dos 10 websites mais relevantes.
def getTop10WebsitesInfo(top_10):
    conn = sqlite3.connect('SQL.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT website_title, url, website_content FROM websites WHERE website_id IN {top_10}")
    r = cursor.fetchall()
    return r



def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d






# Initialize Flask App
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'




@app.route('/')
@cross_origin()
def main_page():
    return jsonify({"response": "Resposta"})




@app.route('/Search')
@cross_origin()
def display_data():
    global all_data
    search_string = str(request.args.get('searchString'))
    tfidflists = getTfidfLists(search_string)
    top_10 = getBestWebsites(tfidflists)
    websitesInfo = getTop10WebsitesInfo(top_10)
    return jsonify({'Search': websitesInfo })



port = int(os.environ.get('PORT', 8080))




if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=port)