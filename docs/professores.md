# Professores

Este é um tutorial para você que é professor e deseja utilziar nosso servidor para cadastrar desafios para seus alunos.

## Tutoriais

### 1. Adicionando novos usuários

A adição de alunos é feita através do script `adduser.py`. Ele pode ser acessado [clicando aqui](https://github.com/gabrielzezze/softdes-desafios/blob/main/src/adduser.py).

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

**Lembrete**: A senha padrão e inicial de todo usuário é seu proprio _username_.

### 2. Adicionando novos desafios

A adição de desafios ocorre através de um sqcript `.sql`.

A estrutura de um quiz é a que segue:

- _numb_: Inteiro que indica o número do quiz;
- _release_: Texto no formato `YYYY-MM-DD`. Indica a data de início do teste;
- _expire_: Texto no formato `YYYY-MM-DD HH:MM:SS`. Indica a data limite para a realização do teste;
- _problem_: Texto de descrição do problema;
- _tests_: Texto no formato de array, onde cada item da array é um teste a ser realizado;
- _results_: Texto no formato de array, onde cada item da array é o resultado esperado pelo teste;
- _diagnosis_: Texto no formato de array, onde cada item da array é o feedback recebido pelo aluno caso ele não acerte o teste;

**Lembrete**: A ordem das arrays `tests`, `results` e `diagnosis` importa! Você deve casar a posição desejada da tripla de teste, resultado e diagnóstico.

Tendo em mãos essa informações, é possível inserir um novo desafio no sistema através do seguinte comando:

```bash
sqlite3 quiz.db 'Insert into QUIZ(numb, release, expire, problem, tests, results, diagnosis) values (_numb, _release, _expire, _problem, _tests, _results, _diagnosis);'
```

Como referência, tenha o exemplo abaixo:

```bash
sqlite quiz.db "Insert into QUIZ(numb, release, expire, problem, tests, results, diagnosis) values (1, '2021-08-10','2021-12-31 23:59:59','Exemplo de problema','[[1],[2],[3]]','[0, 0, 0]','[\"a\",\"b\",\"c\"]')";
```
