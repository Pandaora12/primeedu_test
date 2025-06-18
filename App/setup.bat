@echo off
echo Criando ambiente virtual...
python -m venv venv

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependências...
pip install -r requirements.txt

echo Configuração concluída!
echo.
echo Para iniciar a API Flask:
echo python run.py
echo.
echo Para iniciar o Streamlit:
echo streamlit run streamlit_app.py
echo.
echo Pressione qualquer tecla para sair...
pause > nul