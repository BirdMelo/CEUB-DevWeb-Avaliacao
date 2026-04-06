# Sistema de Gerenciamento de Rotinas Pessoais

## Descrição do Sistema

Este projeto consiste em uma aplicação backend desenvolvida para o gerenciamento de rotinas pessoais. O sistema permite que os usuários se cadastrem na plataforma e registrem suas atividades recorrentes diárias, como momentos de estudo, práticas de exercícios físicos, entre outras. 

A aplicação oferece as seguintes funcionalidades principais:
* **Gestão de Rotinas:** Criação, listagem e alternância de status (ativação e desativação) das rotinas cadastradas.
* **Registro de Execução:** Acompanhamento e registro diário da execução de cada rotina do usuário.
* **Trilha de Auditoria (Logs):** Registro de todas as ações relevantes realizadas no sistema, incluindo a criação de novas rotinas, marcação de execuções e alterações de status das atividades.

O foco central da aplicação é garantir a consistência dos dados do usuário por meio de validações rigorosas que controlam o estado atual das rotinas e a frequência de seus registros diários.

## Explicação das Tabelas

O banco de dados (`db_rotinas`) foi modelado de forma relacional e simples, composto por 4 tabelas principais:

* **usuario:** Armazena os dados básicos de quem usa o sistema (`idusuario`, `nome`, `criado_em`). Como é um sistema simplificado, não exige senha.
* **rotina:** Guarda as atividades criadas pelo usuário. Possui um vínculo direto com o criador (`usuario_idusuario`), o nome da atividade e um indicador (`ativa`) para saber se a rotina está em andamento ou pausada.
* **execucoes:** Registra cada vez que uma rotina é concluída no dia. Vincula-se à rotina executada (`rotina_idrotina`) e guarda a data exata da execução (`data_execucao`). 
* **historico_acoes:** Tabela de log e auditoria. Salva o histórico de eventos importantes (`tipo_acao`), vinculando a ação ao usuário e à rotina correspondente, além do momento exato do ocorrido.

## Lista de Rotas
* **home (/)**: página inicial para registrar usuário ou fazer login
### Usuário
* **register (/user/register)**: página para fazer cadastro do usuário
* **login (/user/login)**: página pra entrar com uma conta já existente
* **update (/user/update)**: página para alterar os dados do usuário
* **delete (/user/delete/{int:user_id})**: página para deletar o usuário
## Explicação das Regras de Negócio

O sistema foi desenhado para garantir a consistência no acompanhamento das rotinas e manter um registro confiável de auditoria. As principais regras de negócio implementadas são:

1. **Unicidade de Execução Diária:** * Uma rotina só pode ser registrada como "concluída" ou "executada" uma única vez por dia.
   * O banco de dados garante essa integridade através de uma restrição única (`UniqueConstraint`) cruzando o ID da rotina e a data da execução. Tentativas de registrar a mesma rotina duas vezes no mesmo dia serão bloqueadas.

2. **Validação de Status da Rotina (Ativa/Inativa):**
   * Apenas rotinas com o status "ativo" (`is_active = True`) podem receber novos registros de execução.
   * Rotinas desativadas ou pausadas servem apenas para consulta de histórico, evitando inconsistências nos dados de progresso atual do usuário.

3. **Auditoria Contínua (Trilha de Logs):**
   * Nenhuma alteração crítica pode passar despercebida. Todas as ações do tipo `CREATE` (Criação), `UPDATE` (Atualização) e `DELETE` (Remoção) realizadas no sistema devem obrigatoriamente gerar um registro imutável na tabela `historico_acoes`.
   * Esse registro guarda o autor da ação, qual rotina foi afetada (se aplicável), a descrição do evento e o carimbo exato de data e hora (`created_at`).

4. **Integridade Relacional (Exclusão Segura):**
   * Para evitar registros "órfãos" no banco de dados, a exclusão de um usuário não pode ser feita de forma arbitrária.
   * Ao deletar um usuário, o sistema deve garantir que o histórico de ações atrelado a ele seja devidamente tratado ou limpo primeiro, respeitando as chaves estrangeiras (Foreign Keys).

## Instruções para Execução do Projeto

### Criação do arquivo `.env`
É necessario a criação de um arquivo `.env` para configuração do banco de dados.
Crie uma um arquivo com o nome `.env` e coloquei as seguintes variáveis:
* DB_USER = {nome_do_perfil_do_usuário}
* DB_PASSWORD = {senha_de_acesso}
* DB_HOST = localhost
* DB_PORT = 3306 (ou outra porta configurada)
* DB_NAME = {nome_do_db}

### Bibliotecas a serem baixadas
Copie o codigo abaixo no terminal, dentro do ambiente `(venv_desenvolvimento)`:
```
pip install flask flask-sqlalchemy pymysql python-dotenv flask-migrate
```