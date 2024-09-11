import duckdb
from flask import Flask, request, jsonify

app = Flask(__name__)
con = duckdb.connect('my_database.duckdb')

@app.route('/query', methods=['POST'])
def query_duckdb():
    query = request.json.get('query')
    try:
        result = con.execute(query).fetchdf()
        return result.to_json(orient='split')
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=5000)
