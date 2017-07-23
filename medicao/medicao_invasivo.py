# Simple example of reading the MCP3008 analog input channels and 
# printing them all out. Author: Tony DiCola License: Public Domain
import time
import datetime
import string
import requests

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
#CLK  = 23
#MISO = 21
#MOSI = 19
#CS   = 24
#mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
canal_leitura = 5
tensao = 0
medicao = 0
sumV = 0
contador = 0
offset = 512
n = 0
sensibilidade = 0.066
acc = 0

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)      

while contador < 10:
	acc += mcp.read_adc(canal_leitura)
	contador = contador + 1
offset = acc/10

#period = 1/60
#t_start = time.time()
#count = 0
tempo_intervalo = 500
contador_amostra = 0
dados_consumo={
	'tensao': [],
	'corrente': [],
	'data_medicao': [],
	'id_boltz': 1,
	'num_seq': -1
}

contador_mult = 1
ativo = False

while True:
    end = False
    #amostras = 500
    contador = 0
    tempo_inicial = time.time()*1000
    while time.time()*1000 <= (tempo_inicial + tempo_intervalo):
    #for n in range(1,amostras - 1):  
       # Read all the ADC channel values in a list.
       values = [0]*8
       contador += 1
       for i in range(8):
           # The read_adc function will get the value of the specified channel (0-7).
           values[i] = mcp.read_adc(i)
       medicao = values[canal_leitura]
       #offset = offset + (medicao - offset)/1024
       tensao = medicao - offset
       sqV = tensao*tensao
       sumV += sqV
    Vrms = (sumV/contador)**(0.5)
    Irms = (5.0/1023)*Vrms/sensibilidade
       # Print the ADC values.
       #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
       # Pause for half a second.
    sumV = 0
    if (ativo == False):
	if Irms >= 0.2:
		ativo = True
		dados_consumo['num_seq'] += 1
	else:
		ativo = False
    else:
	if Irms < 0.2:
		print ("Passou")
		end = True
		ativo = False

    if ativo:
    	contador_amostra += 1
  	dados_consumo['tensao'].append(220)
	dados_consumo['corrente'].append(Irms)
	dados_consumo['data_medicao'].append(str(datetime.datetime.now()))
    	if contador_amostra%10 == 0:
		print dados_consumo
		dados_consumo['tensao'] = []
		dados_consumo['corrente'] = []
		dados_consumo['data_medicao'] = []
		contador_mult += 1
		email = "maximillianfx@gmail.com"
		senha = "220494max"
		cabecalho = {'from': email, 'password': senha}
		URL = 'http://192.168.42.59:8000/v1/autorizar'
		URL_consumo = 'http://192.168.42.59:8000/v1/consumo/'
		medicoes_url = '/medicoes/'
		response_auth = requests.get(URL, headers=cabecalho)
		token = str(response_auth.headers['app_token'])
		print token
		cabecalho2 = {'authorization': "token " + token}
		URL_final = URL_consumo + "1" + medicoes_url
		response_post =  requests.post(URL_final,headers=cabecalho2,data=dados_consumo)
		if response_post.status_code != 201:
			print ("Fallha")
    else:
	print ("Oi")
	if end:
		print ("Ola")
		restantes = (10*contador_mult) - contador_amostra
		for m in range(restantes):
			dados_consumo['tensao'].append(220)
			dados_consumo['corrente'].append(0)
			dados_consumo['data_medicao'].append(str(datetime.datetime.now()))
			contador_amostra += 1
			end = False
		print(dados_consumo)
		#print Irms
    		#print contador
    		#time.sleep(0.0002)  
