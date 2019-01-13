int trigger1=7;
int echo1=8;
int dist,distR;
long timetaken;

void setup() {
  // put your setup code here, to run once:
 pinMode(trigger1,OUTPUT);
 pinMode(echo1,INPUT);   
 Serial.begin( 2400);
}

void distcalc(){
  digitalWrite(trigger1,LOW);
  delayMicroseconds(2);
  digitalWrite(trigger1,HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger1,LOW);
  timetaken=pulseIn(echo1,HIGH);
  dist=timetaken*0.034/2;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  distcalc();
  distR=dist;
  if (distR>0 && distR<=20){
    Serial.println("L") ; 
  }
  else if (distR>20 && distR<40){
    Serial.println("R") ;  
  }
  else{
    Serial.println("x");
  }
  delay(500);
}
