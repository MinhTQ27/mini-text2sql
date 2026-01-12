from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, MetaData, Table, select, update, delete
import json, yaml, os
from dotenv import load_dotenv

load_dotenv()


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f'postgresql://{os.getenv("POSTGRES_USERNAME")}:{os.getenv("POSTGRES_PASSWORD")}@127.0.0.1:5432/{os.getenv("POSTGRES_DB")}'
)

db.init_app(app)

# Reflect once at startup
with app.app_context():
    metadata = MetaData()
    metadata.reflect(bind=db.engine)


@app.route("/get_tables", methods=["GET"])
def get_tables():
    tables = list(metadata.tables)
    return jsonify(tables)


@app.route("/get_columns/<table_name>", methods=["GET"])
def get_columns(table_name):
    columns = [col.name for col in metadata.tables[table_name].columns]
    return jsonify(columns)


@app.route("/get_records/<table_name>", methods=["GET"])
def get_all(table_name):
    # table = Table(table_name, metadata, autoload_with=db.engine)
    table = metadata.tables[table_name]
    sql_statement = select(table)
    records = db.session.execute(sql_statement).fetchall()

    data = [dict(record._mapping) for record in records]  # Convert records to list of dicts
    return jsonify(data)


@app.route("/get_limit_records/<table_name>/<num_records>")
def get_limit(table_name, num_records):
    table = metadata.tables[table_name]
    sql_statement = select(table).limit(num_records)
    records = db.session.execute(sql_statement).fetchall()
    
    data = [dict(record._mapping) for record in records]
    return jsonify(data)


@app.route("/delete/<table_name>", methods=["POST"])
def delete_table(table_name):
    record = request.args.to_dict()
    s = record["record"].replace("'", '"')
    record_dict = json.loads(s)
    delete(table_name).where(record_dict)


@app.route("/delete_record/<table_name>", methods=["POST"])
def delete_record(table_name):
    condition = request.form.get("condition")
    table = metadata.tables[table_name]
    sql_statement = delete(table).where(condition)
    db.session.execute(sql_statement)
    return {"hihi": "hihi"}
    # return result
    # if result > 0: return jsonify({"status": "deleted"}), 200
    # else: return jsonify({'state': 'failed'})


if __name__ == "__main__":
    app.run("127.0.0.1", 5555, debug=True)
