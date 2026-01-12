import os
from dotenv import load_dotenv
import psycopg
from openai import OpenAI
import yaml
load_dotenv()

with open("configs.yaml", "r") as f:
    configs = yaml.safe_load(f)

class Text2Sql:
    def __init__(self, usr, pwd, db, api_key, url):
        self.__client = OpenAI(api_key=api_key, base_url=url)
        self.__conn = psycopg.connect(
            dbname=db,
            user=usr,
            password=pwd,
            host='postgres_db', # The name of db service in docker-compose.yml
            port='5432'
        )

    def get_schema_description(self):
        schema_description = ''

        cur = self.__conn.cursor()
        table_names = cur.execute(configs['QUERY_TABLE_NAME']).fetchall()
                
        for table_name_tuple in table_names:
            table_description = f'Table {table_name_tuple[0]}:\nColumns:\n' 
                    
            cur.execute(configs['QUERY_COLUMN_DETAIL'], table_name_tuple)
            for col_name_and_type in cur.fetchall():
                table_description += f'   - {col_name_and_type[0]}: {col_name_and_type[1]}\n'
                    
            schema_description += table_description

        return schema_description

    def generate_sql(self, model_name, user_question):
        system_prompt = configs['TEXT2SQL_PROMPT']
        system_prompt += self.get_schema_description()
        system_prompt += configs['FEW_SHOT_TEXT2SQL']

        sql_response = self.__client.responses.create(
            model        = model_name,
            instructions = system_prompt,
            input        = [{"role": "user", "content": user_question}]
        )

        def extract_sql(response=sql_response.output_text):
            import re

            pattern = r"```sql\s*(.*?)\s*```"
            match = re.search(pattern, response, re.DOTALL)

            if match: code = match.group(1)
            else: code=response

            return code
        
        return extract_sql()
    
    def generate_insight(self, model_name, user_question, sql_query, query_result):
        prompt = configs['INSIGHT_PROMPT'].format(
            user_question = user_question,
            sql_query = sql_query,
            query_result = query_result
        )

        insight_response = self.__client.responses.create(
            model = model_name,
            input = prompt
        )

        return insight_response.output_text
    
    def execute_sql(self, sql_query):
        with self.__conn.cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()  