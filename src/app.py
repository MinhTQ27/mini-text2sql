from flask import Flask, render_template, request
import requests, json

app = Flask(__name__)

def get_tables():
    tables = requests.get('http://127.0.0.1:5555/get_tables')
    return tables.json()

def get_table_data(table_name, num_records):
    records = requests.get(f'http://127.0.0.1:5555/get_limit_records/{table_name}/{num_records}')
    cols = requests.get(f'http://127.0.0.1:5555/get_columns/{table_name}')
    return cols.json(), records.json()
  
@app.route('/')
def home():
    tables = get_tables()
    first_table = tables[0]
    first_table_cols, first_table_records = get_table_data(first_table, 5)
    return render_template('index.html', tables=tables, columns=first_table_cols, records=first_table_records)


@app.route('/test')
def test():
    table_cols, table_records = get_table_data('actor', 10)
    return render_template('components/data-display.html', columns=table_cols, records=table_records)


# @app.route('/')
# def home():
#     tables_response = requests.get('http://127.0.0.1:5555/get_tables')
#     tables = tables_response.json()
#     return render_template('index.html', tables=tables, get_all_table=get_all_table)

# @app.route('/get_all/<table_name>')
# def get_all_table(table_name):
#     records = requests.get(f'http://127.0.0.1:5555/get_all/{table_name}')
#     cols = requests.get(f'http://127.0.0.1:5555/get_columns/{table_name}')
#     records = records.json()
#     cols = cols.json()
#     return render_template('table_page.html', table=table_name, columns=cols, records=records)

@app.route('/edit_form/<table_name>', methods=['POST'])
def get_edit_form(table_name):
    cols = requests.get(f'http://127.0.0.1:5555/get_columns/{table_name}')
    cols = cols.json()
    # record = request.form.get('record')
    record = request.args.to_dict()

    # import json

    # s = record['record'].replace("'", '"')
    # record_dict = json.loads(s)
    print(type(record))
    # for col in cols: 
    #     print(record[col])

    return render_template('data-display.html', table=table_name, columns=cols, record=record)

@app.route('/delete_record/<table_name>', methods=['POST'])
def delete_record(table_name):
    # delete_condition = request.args.to_dict()
    delete_condition = request.form.get('delete_condition')
    delete_condition = json.loads(delete_condition)

    delete_condition = delete_condition['delete_condition'].replace("'", '"')
    result = requests.post(f'http://127.0.0.1:5555/delete_record/{table_name}',
                  data=delete_condition)
    return result

if __name__ == "__main__":
    app.run("127.0.0.1", 8000, debug=True)