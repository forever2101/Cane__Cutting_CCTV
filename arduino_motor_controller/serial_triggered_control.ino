
// Define stepper motor connections and steps per revolution:
int dDelay = 10;
const int PinYPul =  2;  //MY
const int PinYDir =  3;  //
const int PinXPul =  4;  //MX
const int PinXDir =  5;  //
const int Relay1 =  9;  // cut dri
#define motor_y_steps 50
#define motor_x_steps 50
#define motor_y_steps_cane 50
#define sensorhome_X  8  //home x
#define sensorhome_Y  6  //home y
#define sensorhome_C  7  //Cut  x  //Cut_X <==============> sensorhome_X
int sensorVal_x; 
int sensorVal_y; 
int sensorVal_c; 

void setup() {
  // Declare pins as output:
  pinMode(PinYPul, OUTPUT);  //Y
  pinMode(PinYDir, OUTPUT);  //Y
  pinMode(PinXPul, OUTPUT);  //X
  pinMode(PinXDir, OUTPUT);  //X
  pinMode(sensorhome_X, INPUT_PULLUP); //7
  pinMode(sensorhome_Y, INPUT_PULLUP); //6
  pinMode(sensorhome_C, INPUT_PULLUP); //8
  Serial.begin(9600);
  Serial.println("Starting...");
  CheckHomeX();
  CheckHomeY();
}

//  Initialize some working variables
char in_byte = ' ';
int in_num;

/*
 * Expecting an ASCII character of an integer ('0' --> '9') as serial input, 
 * returns that ASCII integer as an int.
 */
int get_serial_input_as_int() {
  in_byte = Serial.read();
  return int(in_byte - '0');  //  Input is ASCII character of a single digit integer. Convert to int.
}

void loop() {
  char user_input;   
  while(Serial.available())
  {
    user_input = Serial.read(); //Read user input and trigger appropriate function
     
    if (user_input =='1')
    {
      Serial.println("Mx for ");
      digitalWrite(PinXDir, HIGH);
      for (int i = 0; i < 1000; i++) {
        pulseX();
        Serial.println(i);
      } 
      Serial.println("out Mx ");            
    }
    else if(user_input =='2')
    {
      Serial.println("Mx Rev ");
      digitalWrite(PinXDir, LOW);
      for (int i = 0; i < 1000; i++) {
        pulseX();
        Serial.println(i);
      } 
      Serial.println("out Mx ");            
    }
    else if(user_input =='3')
    {
      Serial.println("My for ");
      digitalWrite(PinYDir, HIGH);
      for (int i = 0; i < 500; i++) {
          pulseY();
          Serial.println(i);
      } 
        Serial.println("out My ");          
    }
    else if(user_input =='4')
    {
      Serial.println("My Rev ");      
      digitalWrite(PinYDir, LOW);
      for (int i = 0; i < 500; i++) {
           pulseY();
           Serial.println(i);
      } 
      Serial.println("out My ");        
    }
    else if(user_input =='5')
    {
      Serial.println("CUT ");
       while(digitalRead(sensorhome_C) == HIGH) //8
          {
            delay(5);
            digitalWrite(PinXDir, HIGH); //PinYDir
             pulseX();
          }
          delay(2000); //delay stop cut SAW
       while(digitalRead(sensorhome_X) == HIGH) //8
         {
           delay(5);
           digitalWrite(PinXDir, LOW); //PinYDir
           pulseX();
         }
       delay(200);
    } ///
    else if(user_input =='6')
     {
      Serial.println("My stop ");
      digitalWrite(PinYDir, LOW);
           //Serial.println("out My ");          
    }
    else if(user_input =='7')
     {
      Serial.println("Mx stop ");
      digitalWrite(PinXDir, LOW);
           //Serial.println("out Mx ");          
    }else if(user_input =='8')
     {
      Serial.println("Check Home X ");
      CheckHomeX();
    }
    else if(user_input =='9')
     {
      Serial.println("Check Home Y");
      CheckHomey();
    }
    else
    {
      Serial.println("EXIT");
    }
      
  }
}

void pulseX()
{
  digitalWrite(PinXPul, LOW); // pin 4
  delayMicroseconds(dDelay);
  digitalWrite(PinXPul, HIGH);
  delayMicroseconds(dDelay);
}
void pulseY()
{
  digitalWrite(PinYPul, LOW); //pin 2
  delayMicroseconds(dDelay);
  digitalWrite(PinYPul, HIGH);
  delayMicroseconds(dDelay);
}

void CheckHomeX()
{
  Serial.println("Set Home X Position");
  delay(100);
  
  while(digitalRead(sensorhome_X) == HIGH) //7
  {
    delay(5);
    digitalWrite(PinXDir, LOW); //PinYDir
    pulseX();
  }
  delay(100);
}
void CheckHomeY()
{
  Serial.println("Set Home Y Position ");
  delay(100);
  while(digitalRead(sensorhome_Y) == HIGH) // pin 6
  {
    delay(5);
    digitalWrite(PinYDir, LOW);
    pulseY();
  }
  delay(100);
}
