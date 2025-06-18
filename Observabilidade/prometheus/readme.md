# README do Prometheus

Este arquivo README fornece informações sobre a configuração do Prometheus dentro do projeto de observabilidade.

## Visão Geral

O Prometheus é uma ferramenta de monitoramento e alerta de código aberto, projetada para confiabilidade e escalabilidade. Neste projeto, o Prometheus está configurado para coletar métricas do exportador PostgreSQL, que reúne dados de desempenho do banco de dados PostgreSQL.

## Dockerfile

O `Dockerfile` neste diretório contém as instruções necessárias para construir uma imagem Docker para o Prometheus. Ele configura o ambiente do Prometheus e utiliza o arquivo de configuração `prometheus.yml` para definir como as métricas são coletadas.

## Construindo a Imagem Docker

Para construir a imagem Docker do Prometheus, navegue até o diretório `prometheus` e execute o seguinte comando:

```bash
docker build -t prometheus-image .
```

## Executando o Prometheus

O Prometheus pode ser executado como um contêiner usando o Docker. O seguinte comando iniciará o Prometheus, expondo-o na porta 9090:

```bash
docker run -d -p 9090:9090 prometheus-image
```

Certifique-se de que o exportador PostgreSQL esteja em execução e acessível para que o Prometheus possa coletar métricas com sucesso.

## Configuração

O arquivo `prometheus.yml` contém a configuração do Prometheus, incluindo o trabalho de coleta (scrape job) para o exportador PostgreSQL. Você pode modificar este arquivo para ajustar os intervalos de coleta ou adicionar outros alvos de coleta, conforme necessário.

## Acessando o Prometheus

Depois que o Prometheus estiver em execução, você pode acessar a interface web navegando para `http://localhost:9090` no seu navegador. A partir daí, você pode explorar as métricas coletadas e criar alertas com base nas suas necessidades de monitoramento.

## Conclusão

Esta configuração permite monitorar o banco de dados PostgreSQL de forma eficaz usando o Prometheus. Para uma integração adicional com ferramentas de visualização, considere usar o Grafana, que pode ser configurado para exibir as métricas coletadas pelo Prometheus.