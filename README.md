# NLP


## Guia de uso

### Clone o repositório
#### No diretório NlpSearcher, execute o comando "flask run"
#### No diretório NlpSearcher/nlp_search, execute o comando npm install e em sequência npm start
#### Se o navegador não abrir automaticamente, acesse o endereço http://localhost:3000/


## Descrição dos arquivos
### WebcrawlerNotebook: WebCrawler para coleta de urls, título das páginas e seus conteúdos e criação do Database
### DBManager: Criação e preenchimento das tabelas do Database
### App.py: Aplicação Web com endpoints e funções de busca no banco de dados. A implementação da lista invertida e da Levenshtein distance se encontram nesse arquivo
### nlp_search: Pasta com arquivos da página web em React
