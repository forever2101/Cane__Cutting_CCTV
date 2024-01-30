#include "HX711.h"

#define DOUT  A3
#define CLK   A2
#define DEC_POINT  3
#define MotorOut 7

// this will be modifed by testing..
#define Offset  0 // unit: g
//#define Lscale  27000/200 // 1/453.592  // unit: g
#define Lscale  273/20.6 // 1/453.592  // unit: g

HX711 scale(DOUT, CLK);

void setup() 
{
  Serial.begin(115200);
  pinMode(MotorOut, OUTPUT);
  digitalWrite(MotorOut, HIGH);

  Serial.println("Load Cell");
  Serial.print("read average: \t\t");
  Serial.println(scale.read_average(20));  	// print the average of 20 readings from the ADC

  // scale.set_offset(Offset);     
  scale.tare();				       // reset the scale to 0
  scale.set_scale(Lscale);       // this value is obtained by calibrating the scale with known weights; see the README for details

  Serial.print("get units: \t\t");
  Serial.println(scale.get_units(5), 3);        // print the average of 5 readings from the ADC minus tare weight, divided
						                                    // by the SCALE parameter set with set_scale
  Serial.println("Readings:");
}


void loop() 
{ 
  Serial.print("Current weight: \t\t");
  long value = scale.get_units(1);  //dummy measurment
  double weightTemp[3];
  value = scale.get_units(8);
  weightTemp[0] = (double)(value) * 0.1;
  value = scale.get_units(8);
  weightTemp[1] = (double)(value) * 0.1;
  value = scale.get_units(8);
  weightTemp[2] = (double)(value) * 0.1;

  //sort
  double weight;
  if( weightTemp[0] < weightTemp[1] )
  {
    weight = weightTemp[0];
    weightTemp[0] = weightTemp[1];
    weightTemp[1] = weight;
  }
  if( weightTemp[1] < weightTemp[2] )
  {
    weight = weightTemp[1];
    weightTemp[1] = weightTemp[2];
    weightTemp[2] = weight;
  }
  if( weightTemp[0] < weightTemp[1] )
  {
    weight = weightTemp[0];
    weightTemp[0] = weightTemp[1];
    weightTemp[1] = weight;
  }
  weight = weightTemp[1]; //select a center value
  double wei = weight;
  Serial.print(wei, DEC_POINT);
  Serial.println(" g");
  if (wei >= 0){
    if(wei < 150){
      ActMotor();
      StopMotor(); 
      delay(50);
    }else if(wei <180){
      ActMotor();
      delay(50);  
      StopMotor();   
      delay(30); 
    }else if(wei <200){
      ActMotor();
      delay(25);  
      StopMotor();   
      delay(15); 
    }else{ delay(100);  
     
      //Serial.print("exceeded weight: \t\t");
      //Serial.println("waiting for other container...");
      delay(10); 
    }
  }
}   
  
void ActMotor(){
  digitalWrite(MotorOut, LOW); // this means max speed rotating.
}
void StopMotor(){
  digitalWrite(MotorOut, HIGH);  
}
