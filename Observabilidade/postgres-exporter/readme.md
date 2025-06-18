# README do Exportador PostgreSQL

## Visão Geral

O Exportador PostgreSQL é uma ferramenta que coleta métricas de um banco de dados PostgreSQL e as expõe em um formato que pode ser coletado pelo Prometheus. Isso permite monitorar o desempenho e a saúde do banco de dados PostgreSQL.

## Propósito

Este exportador foi projetado para fornecer insights sobre várias métricas, como conexões ao banco de dados, desempenho de consultas e uso de recursos. Ao integrá-lo com o Prometheus, você pode configurar alertas e visualizar as métricas no Grafana.

## Construindo a Imagem Docker

Para construir a imagem Docker para o exportador PostgreSQL, navegue até o diretório `postgres-exporter` e execute o seguinte comando:

```bash
docker build -t postgres-exporter .
```

## Executando o Exportador

Depois de construir a imagem, você pode executar o exportador PostgreSQL usando o seguinte comando:

```bash
docker run -d \
  --name postgres-exporter \
  -e DATA_SOURCE_NAME="user=seu_usuario password=sua_senha host=db port=5432 dbname=seu_banco" \
  -p 9187:9187 \
  postgres-exporter
```

Substitua `seu_usuario`, `sua_senha` e `seu_banco` pelas credenciais e nome do banco de dados PostgreSQL. O `host` deve apontar para o serviço PostgreSQL definido na sua configuração do Docker Compose.

## Configuração

O exportador coletará automaticamente métricas do banco de dados PostgreSQL com base no `DATA_SOURCE_NAME` fornecido. Certifique-se de que o usuário PostgreSQL tenha as permissões necessárias para acessar as métricas.

## Acessando as Métricas

Depois que o exportador estiver em execução, você pode acessar as métricas no seguinte URL:

```
http://localhost:9187/metrics
```

Este endpoint fornecerá uma lista de métricas que o Prometheus pode coletar.

## Conclusão

O Exportador PostgreSQL é um componente crucial para monitorar seu banco de dados PostgreSQL. Ao integrá-lo com o Prometheus e o Grafana, você pode obter insights valiosos sobre o desempenho e a saúde do seu banco de dados.