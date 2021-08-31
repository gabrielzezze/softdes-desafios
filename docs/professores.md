Uma página de guia de usuário para professores. Ela deverá descrever:
    como adicionar usuários (usando os arquivos users.csv e add_user.py)
    como adicionar novos desafios (linha de comando mesmo) -->
# Professores

Este é um tutorial para você que é professor e deseja utilziar nosso servidor para cadastrar desafios para seus alunos.

## Tutoriais

### 1. Adicionando novos usuários

A adição de alunos é feita através do script `adduser.py`. Ele pode ser acessado [clicando aqui](../src/adduser.py).

Para utilizá-lo, tenha em mãos as informações dos usuários que serão adicionados. Estes devem estar em um arquivo denominado `users.csv`, colocado no mesmo diretório que o script.

Cada liha deste arquivo representa um usuário. A linha deve conter duas informações:

1. O nome de usuário
2. O tipo do usuário (admin, aluno ou professor)

Abaixo um exemplo de csv.

```csv
admin,admin
gabriel,aluno
```

Neste caso, rodando o script teremos os usuários `admin` e `gabriel` adicionados na base de dados. 

**Lembrete**: A senha padrão e inicial de todo usuário é seu proprio *username*.

### 2. Adicionando novos desafios

A adição de desafios ocorre através de um sqcript `.sql`.

A estrutura de um quiz é a que segue:

- *numb*: Inteiro que indica o número do quiz;
- *release*: Texto no formato `YYYY-MM-DD`. Indica a data de início do teste;
- *expire*: Texto no formato `YYYY-MM-DD HH:MM:SS`. Indica a data limite para a realização do teste;
- *problem*: Texto de descrição do problema;
- *tests*: Texto no formato de array, onde cada item da array é um teste a ser realizado;
- *results*: Texto no formato de array, onde cada item da array é o resultado esperado pelo teste;
- *diagnosis*: Texto no formato de array, onde cada item da array é o feedback recebido pelo aluno caso ele não acerte o teste; 

**Lembrete**: A ordem das arrays `tests`, `results` e `diagnosis` importa! Você deve casar a posição desejada da tripla de teste, resultado e diagnóstico.

Tendo em mãos essa informações, é possível inserir um novo desafio no sistema através do seguinte comando:

```bash
sqlite3 quiz.db 'Insert into QUIZ(numb, release, expire, problem, tests, results, diagnosis) values (_numb, _release, _expire, _problem, _tests, _results, _diagnosis);'
```

Como referência, tenha o exemplo abaixo:

```bash
sqlite quiz.db "Insert into QUIZ(numb, release, expire, problem, tests, results, diagnosis) values (1, '2021-08-10','2021-12-31 23:59:59','Exemplo de problema','[[1],[2],[3]]','[0, 0, 0]','[\"a\",\"b\",\"c\"]')";
```
