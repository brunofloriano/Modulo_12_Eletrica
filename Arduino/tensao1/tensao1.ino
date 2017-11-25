int medicao = 5;
int val = 0;
float medicao_analog = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //pinMode(medicao, OUTPUT); 
}

void loop() {
  // put your main code here, to run repeatedly:

  val = analogRead(medicao);   // turn the LED on (HIGH is the voltage level)
  medicao_analog = tensao(val);
  Serial.print(medicao_analog);
  Serial.print("\t"); 
  Serial.print(val,BIN);
  Serial.print("\t"); 
  delay(1000);

}

float tensao(int x){
  float y = (float)x;
  float v = 5*y/1023;
  return v;
  
  }
