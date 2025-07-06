# cliente_api.py
"""
Cliente para interação com a API GraphQL.
Responsável por autenticação e consultas de dados.
"""

import requests
from datetime import datetime
from config import API_URL, API_HEADERS, LOGIN_CREDENTIALS


class ClienteAPI:
    
    def __init__(self):
        self.token = None
        self.headers = API_HEADERS.copy()
    
    def fazer_login(self):
        login_payload = {
            "query": """mutation login($email: String!, $password: String!) {
                logIn(input: { email: $email, password: $password }) {
                    token
                    preAuthToken
                    email
                    role 
                }
            }""",
            "variables": {
                "email": LOGIN_CREDENTIALS["email"],
                "password": LOGIN_CREDENTIALS["password"]
            }
        }
        
        try:
            response = requests.post(API_URL, headers=self.headers, json=login_payload)
            response.raise_for_status()
            
            data = response.json()
            if 'errors' in data:
                raise Exception(f"Erro no login: {data['errors']}")
                
            self.token = data['data']['logIn']['token']
            print("Login realizado com sucesso!")
            print(f"Token obtido: {self.token[:20]}...{self.token[-10:] if len(self.token) > 30 else self.token}")
            return self.token
            
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            raise
    
    def buscar_dados_timesheet(self, data_inicio, data_fim):
        if not self.token:
            raise Exception("Token não encontrado. Faça login primeiro.")
        
        data_inicio_dt = datetime.strptime(data_inicio, "%d/%m/%Y")
        
        periodo = data_inicio_dt.strftime("%Y-%m")
        
        query_payload = {
            "query": """{
                records(where: { 
                    sheet: { key_regex: "timesheet" } 
                    dynamicFields: { start_date_regex: "%s"}
                } order: { updatedAt: DESC}) {
                    count
                    data {
                        id
                        dynamicFields
                        dynamicAssociations
                    }
                }
            }""" % periodo,
            "variables": {}
        }

        headers_auth = self.headers.copy()
        headers_auth['Authorization'] = self.token
        
        try:
            print("Enviando requisição com autenticação padrão...")
            response = requests.post(API_URL, headers=headers_auth, json=query_payload)

            if response.status_code == 200:
                data = response.json()
                if 'errors' not in data:
                    print(f"Dados recuperados com sucesso! Total de registros: {data['data']['records']['count']}")
                    return data['data']['records']['data']
                else:
                    print(f"Erro na consulta: {data['errors']}")
            else:
                print(f"Status {response.status_code} na resposta da API.")
        except requests.exceptions.HTTPError as e:
            print(f"Erro HTTP: {e}")
            raise
        except Exception as e:
            print(f"Erro geral: {e}")
            raise
        raise Exception("Erro ao buscar dados do timesheet.")
