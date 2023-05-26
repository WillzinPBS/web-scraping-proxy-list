import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd
import pyodbc

# Configuro o webdriver para sempre instalar a versão mais atual
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Configuração do Banco de dados
connection_config = (
    "Driver=SQL Server;"
    "Server=DESKTOP-GGHN154\SQLEXPRESS;"
    "Database=BDWill;"
)

connection = pyodbc.connect(connection_config)
cursor = connection.cursor()

query = f"""
    insert into t_Free_Proxy_List
    select
        {'getdate()'}, {'null'}, {0}, {0}, {f"'-'"}
"""

cursor.execute(query)
cursor.commit()

# Entro na url
driver.get('https://proxyservers.pro/proxy/list/order/updated/order_dir/desc')

# Armazeno o html da página em uma variável
dfs = pd.read_html(driver.page_source)

# Número total de páginas
number_of_pages = int(driver.find_element(By.XPATH, '//li[@class="page-item"][10]').text)

for c in range(number_of_pages):
    if c == 0:
        dataframe = dfs[0][['IP Address', 'Port', 'Country', 'Protocol']]
    else:
        # driver.find_element(By.XPATH, '//a[text()="{}"]'.format(c+1)).click()
        driver.get('https://proxyservers.pro/proxy/list/order/updated/order_dir/desc/page/{}'.format(c+1))
        sleep(1)
        dfs = pd.read_html(driver.page_source)
        
        new_dataframe = dfs[0][['IP Address', 'Port', 'Country', 'Protocol']]
        dataframe = pd.concat([dataframe, new_dataframe], ignore_index=True)

json_response = dataframe.to_json(orient='index', indent=4)

with open('FreeProxyList.json') as user_file:
    string_json = user_file.read()

json_file = json.loads(string_json)

# Quantidade de linhas extraídas
number_of_lines = len(json_file) - 1

with open("FreeProxyList.json", "w") as outfile:
    outfile.write(json_response)

query = f"""
    update t_Free_Proxy_List
    set
        dataFimExec         = getdate(),
        qtdPaginasExtraidas = {number_of_pages},
        qtdLinhasExtraidas  = {number_of_lines},
        jsonGerado          = {"'"+string_json+"'"}
"""

cursor.execute(query)
cursor.commit()
