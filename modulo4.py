from faker import Faker
from banco import BancoDados   # importa a classe do outro arquivo

fake = Faker()
bd = BancoDados()
bd.criar_tabela()

# gera 100 registros aleatórios
for _ in range(100):
    bd.inserir_dados(
        fake.text(max_nb_chars=20),  # título curto
        fake.name(),                 # autor
        int(fake.year()),            # ano de publicação
        fake.word()                  # gênero
    )

print("100 registros inseridos com sucesso!")