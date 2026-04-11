import psycopg2
from faker import Faker

class BancoDados:
    def __init__(self):
        self.conexao = psycopg2.connect(
            dbname="Facu",       # nome do banco
            user="postgres",     # usuário
            password="592765",   # senha
            host="localhost"     # servidor
        )
        self.cursor = self.conexao.cursor()
        self.faker = Faker()

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

    def inserir_dados_fake(self, quantidade=5):
        for _ in range(quantidade):
            titulo = self.faker.sentence(nb_words=3)
            autor = self.faker.name()
            ano = int(self.faker.year())
            genero = self.faker.word()
            self.inserir_dados(titulo, autor, ano, genero)

    def listar_livros(self):
        self.cursor.execute("SELECT * FROM livros;")
        for linha in self.cursor.fetchall():
            print(linha)

    def selecionar_dados(self):
        self.cursor.execute("SELECT * FROM livros;")
        return self.cursor.fetchall()


if __name__ == "__main__":
    bd = BancoDados()
    bd.criar_tabela()
    bd.inserir_dados_fake(10)  # insere 10 registros fictícios
    bd.listar_livros()