from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import pandas as pd

# Configuro o webdriver para sempre instalar a versão mais atual
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

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
        # driver.find_element(By.XPATH, '//li[@class="page-item"][{}]'.format(c)).click()
        driver.find_element(By.XPATH, '//a[text()="{}"]'.format(c+1)).click()
        dfs = pd.read_html(driver.page_source)

        new_dataframe = dfs[0][['IP Address', 'Port', 'Country', 'Protocol']]
        dataframe = pd.concat([dataframe, new_dataframe], ignore_index=True)

json_response = dataframe.to_json(orient='index', indent=4)

with open("FreeProxyList.json", "w") as outfile:
    outfile.write(json_response)

# while(True):
#     pass
