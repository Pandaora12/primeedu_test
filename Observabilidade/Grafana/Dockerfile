# Usa a imagem oficial do Grafana como base.
# Essa imagem contém o Grafana pré-instalado e pronto para uso.
FROM grafana/grafana:latest

# Copia o arquivo de dashboard de exemplo para o diretório padrão de dashboards do Grafana.
# O arquivo JSON contém a configuração de um dashboard que será carregado automaticamente.
COPY dashboards/example-dashboard.json /var/lib/grafana/dashboards/example-dashboard.json

# Define uma variável de ambiente para especificar o caminho de provisionamento do Grafana.
# O provisionamento é usado para configurar fontes de dados e dashboards automaticamente.
ENV GF_PATHS_PROVISIONING=/etc/grafana/provisioning