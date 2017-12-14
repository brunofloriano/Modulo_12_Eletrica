//Autor : FILIPEFLOP
 
//Baseado no programa exemplo da biblioteca EmonLib
 
//Carrega as bibliotecas
#include "EmonLib.h"
#include <SPI.h>
 
EnergyMonitor emon1;
 
//Tensao da rede eletrica
int rede = 220;
 
//Pino do sensor SCT
int pino_sct = A1;
 
void setup()
{
  Serial.begin(9600);
  //Pino, calibracao - Cur Const= Ratio/BurdenR. 2000/33 = 60
  emon1.current(pino_sct, 60);
}
 
void loop()
{
  //Calcula a corrente
  int sample = analogRead(pino_sct);
  double Irms = emon1.calcIrms(1480);
  //Mostra o valor da corrente no serial monitor e display
  Serial.print("Corrente : ");
  Serial.println(sample); // Irms
  delay(200);
}

