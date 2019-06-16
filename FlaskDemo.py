#!flask/bin/python
from flask import *
from flask_cors import CORS
from elasticsearch import Elasticsearch

#Flask,jsonify,make_response,request
def autocomplete_course_title(text):
    res_list = []
    es = Elasticsearch()
    res = es.search(index="my_index", body={"query": {"match": {"course_title":text}}})
    for result in res['hits']['hits']:
        res_list.append(result['_source']['course_title'])
    return res_list

def search_results(text):
    res_list = []
    es = Elasticsearch()
    res = es.search(index="my_index",
                    body={"query":
                            {"multi_match" :
                                {
                                    "query": text,
                                    "fields": [ "course_title", "url", "description" ]
                                }
                            }
                    })
    for result in res['hits']['hits']:
        _dict = {}
        if 'course_title' in result['_source']:
            _dict['course_title'] = result['_source']['course_title']
        if 'url' in result['_source']:
            _dict['url'] = result['_source']['url']
        if 'description' in result['_source']:
            _dict['description'] = result['_source']['description']
        res_list.append(_dict)
    return res_list

app = Flask("Flask Demo")

CORS(app)

@app.route('/app/course_title',methods=['POST','GET'])
def get_course_title():
    if request.method == 'POST':
        print("****POST REQUEST****")
        if request.form.get('text'):
            res_list = autocomplete_course_title(str(request.form.get('text')))
            return jsonify({'result':res_list})

    return jsonify({'result':[]})

@app.route('/app/search',methods=['POST'])
def get_search_results():
    if request.method == 'POST':
        print("****POST REQUEST****")
        if request.form.get('text'):
            res_list = search_results(str(request.form.get('text')))
            return jsonify({'result':res_list})

    return jsonify({'result':[]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run() 'Webpage will not show any error regarding code if we dont use debug=True'