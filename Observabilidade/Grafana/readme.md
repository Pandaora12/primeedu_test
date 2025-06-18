# Configuração do Grafana para o Projeto de Observabilidade

Este README fornece informações sobre a configuração do Grafana dentro do projeto de observabilidade. O Grafana é uma ferramenta poderosa para visualizar métricas coletadas de várias fontes de dados, incluindo o Prometheus.

## Propósito

O serviço Grafana é projetado para visualizar métricas coletadas do banco de dados PostgreSQL por meio do exportador PostgreSQL e do Prometheus. Ele permite que os usuários criem dashboards e monitorem a saúde e o desempenho do banco de dados em tempo real.

## Construindo a Imagem Docker

Para construir a imagem Docker do Grafana, navegue até o diretório `grafana` e execute o seguinte comando:

```bash
docker build -t grafana-image .
```

## Executando o Contêiner Grafana

Após construir a imagem, você pode executar o contêiner Grafana usando o seguinte comando:

```bash
docker run -d -p 3000:3000 --name grafana-container grafana-image
```

Este comando iniciará o servidor Grafana, que estará acessível em `http://localhost:3000`. As credenciais padrão de login são:

- **Usuário:** admin
- **Senha:** admin

Você será solicitado a alterar a senha no primeiro login.

## Importando o Dashboard de Exemplo

Depois de iniciar o Grafana, você pode importar o dashboard de exemplo fornecido na pasta `dashboards`. Siga os passos abaixo:

1. Faça login no Grafana.
2. Clique no ícone "+" na barra lateral esquerda e selecione "Importar".
3. Faça o upload do arquivo `example-dashboard.json` ou cole o conteúdo JSON do arquivo.
4. Selecione a fonte de dados Prometheus apropriada e clique em "Importar".

Isso criará um dashboard que visualiza as métricas coletadas do banco de dados PostgreSQL.

## Conclusão

O Grafana é um componente essencial do projeto de observabilidade, fornecendo uma interface amigável para monitorar e analisar métricas. Seguindo as instruções acima, você pode configurar o Grafana e começar a visualizar suas métricas do PostgreSQL de forma eficaz.