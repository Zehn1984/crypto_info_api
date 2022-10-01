# MADE BY ANDERSON CAMPOLINA - RPA AND WEB3 DEV
# EMAIL: andersoncampolina@gmail.com
# LINKEDIN: https://www.linkedin.com/in/anderson-campolina-688175225/
# LINK OF ONLINE API: https://cryptoinfo.ansoapi.repl.co/

from fastapi import FastAPI
import uvicorn
import requests
from bscscan import BscScan #pip install bscscan-python

app = FastAPI()

@app.get("/")
def home():
    return {"Documentation page: https://cryptoinfo.ansoapi.repl.co/docs": "AnsoAPI just have 1 endpoint, and it is: 'https://cryptoinfo.ansoapi.repl.co/contract/' and all you must insert is any contract hash number after the endpoint, and it will return a JSON file"}

@app.get("/contract/{contrato}")
def get_info(contrato):
  #dexscreener
  dexscreener = requests.get('https://api.dexscreener.io/latest/dex/search?q='+contrato)
  dexscreener = dexscreener.json()
  dados_dexscreener = dexscreener['pairs']
  
  #coingecko coinlist
  url = "https://coingecko.p.rapidapi.com/coins/list"
  headers = {
    "X-RapidAPI-Host": "coingecko.p.rapidapi.com",
    "X-RapidAPI-Key": "4975913f71msh47d0b5b7796f6e1p111bfbjsnfb7a1164b2e6"
  }
  lista_moedas_cg = requests.request("GET", url, headers=headers)
  lista_moedas_cg = lista_moedas_cg.json()
  
  #coingecko
  for i in lista_moedas_cg:
    if i['symbol'] == dexscreener['pairs'][0]['baseToken']['symbol'].lower():
        ID_moeda = i['id']
  
  url = "https://coingecko.p.rapidapi.com/coins/" + ID_moeda
  
  querystring = {
    "localization": "true",
    "tickers": "true",
    "market_data": "true",
    "community_data": "true",
    "developer_data": "true",
    "sparkline": "false"
  }
  
  headers = {
    "X-RapidAPI-Host": "coingecko.p.rapidapi.com",
    "X-RapidAPI-Key": "4975913f71msh47d0b5b7796f6e1p111bfbjsnfb7a1164b2e6"
  }
  
  response = requests.request("GET", url, headers=headers, params=querystring)
  response = response.json()
  
  cadastrado_coingecko = False
  lista = list(response['platforms'].values())
  for i in range(len(lista)):
    if lista[i].lower() == contrato.lower():
        cadastrado_coingecko = True
  
  dados_totais = dados_dexscreener
  dados_coingecko = ''
  if cadastrado_coingecko:
    dados_coingecko = response
    dados_coingecko = [dados_coingecko]
    dados_totais = dados_dexscreener + dados_coingecko
  
  # honeypot_scam_protection
  if (dados_dexscreener[0]['txns']['h24']['sells'] / dados_dexscreener[0]['txns']['h24']['buys']) < 0.2:
    dados_totais[0]['is_honeypot'] = True
  else:
    dados_totais[0]['is_honeypot'] = False
  
  # codigo-fonte do contrato (API BSCSCAN)
  if dados_totais[0]['chainId'].lower() == 'bsc':
    bscscan_api_key = 'RVU93JY8QTVZ577VV82W4K5S55KY3DYF7D'
    with BscScan(bscscan_api_key, asynchronous=False) as client:
      dados_totais[0]['codigo_fonte_contrato'] = client.get_contract_source_code(contrato)    

  return dados_totais

uvicorn.run(app,host="0.0.0.0",port="8080")
