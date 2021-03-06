# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

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
canal_leitura = 1
tensao = 0
medicao = 0
sumV = 0
contador = 1
offset = 512.0
n = 0

print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)      

while True:
    amostras = 500
    for n in range(0,amostras - 1):  
       # Read all the ADC channel values in a list.
       values = [0]*8
       for i in range(8):
           # The read_adc function will get the value of the specified channel (0-7).
           values[i] = mcp.read_adc(i)
       medicao = values[canal_leitura]
       #offset = offset + (medicao - offset)/1024
       tensao = medicao - offset
       sqV = tensao*tensao
       sumV += sqV
       Vrms = (sumV/amostras)**(0.5)
       Irms = (2000.0/33.0)*(3.3/1024.0)*Vrms
       # Print the ADC values.
       #print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values))
       # Pause for half a second.
    sumV = 0
    print Irms
    time.sleep(0.0002)  
