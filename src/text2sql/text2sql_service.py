import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from Text2Sql import Text2Sql
# from waitress import serve
load_dotenv()

app = Flask(__name__)

text2sql = Text2Sql(
    os.getenv("POSTGRES_USERNAME"),
    os.getenv("POSTGRES_PASSWORD"),
    os.getenv("POSTGRES_DB"),
    os.getenv("FPT_API_KEY"),
    os.getenv("FPT_MKP_URL")
)

@app.route('/text2sql/sql', methods=['POST'])
def gen_sql():
    model_name = request.form.get('model_name')
    user_question = request.form.get('user_question')
    sql = text2sql.generate_sql(model_name, user_question)
    return jsonify({'sql': sql})

@app.route('/text2sql/insight', methods=['POST'])
def gen_insight():
    model_name = request.form.get('model_name')
    user_question = request.form.get('user_question')
    sql_query = request.form.get('sql')
    query_result = request.form.get('query_result')
    insight = text2sql.generate_insight(model_name, user_question, sql_query, query_result)
    return jsonify({'insight': insight})

@app.route('/text2sql/exec', methods=['POST'])
def get_exec_result():
    sql = request.form.get('sql')
    exec_result = text2sql.execute_sql(sql)
    return exec_result

@app.route('/health_check')
def ping():
    return {"ok": "ok"}

if __name__ == '__main__':
    
    app.run("0.0.0.0", 8080) # or serve(app, host="0.0.0.0")