   import psycopg2 
   from faker import Faker 
 
   class BancoDados: 
       def __init__(self): 
           self.conexao = psycopg2.connect( 
               dbname="sua_base_de_dados", 
               user="seu_usuario", 
               password="sua_senha", 
               host="localhost" 
           ) 
           self.cursor = self.conexao.cursor() 
        
       def criar_tabela(self): 
           self.cursor.execute(""" 
               CREATE TABLE IF NOT EXISTS livros ( 
                   id SERIAL PRIMARY KEY, 
                   titulo VARCHAR(255), 
                   autor VARCHAR(255), 
                   ano_publicacao INTEGER, 
                   genero VARCHAR(100) 
               ) 
           """) 
           self.conexao.commit() 
 
       def inserir_dados(self, titulo, autor, ano_publicacao, genero): 
           self.cursor.execute(""" 
               INSERT INTO livros (titulo, autor, ano_publicacao, genero) 
               VALUES (%s, %s, %s, %s) 
           """, (titulo, autor, ano_publicacao, genero)) 
           self.conexao.commit()