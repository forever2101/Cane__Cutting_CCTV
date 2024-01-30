//  Define serial input flags
const int MOVE_FLAG = 1;  // Send a character '1' over serial to move horizontal-axis motor and stop rotation motor
const int CUT_FLAG = 2; // Send a character '2' over serial to stop horizontal-axis motor and run rotation motor

// Define stepper motor connections and steps per revolution:

#define dirPin1 3
#define stepPin1 2
#define stepsPerRevolution 200
#define frequency 50

#define dirPin2 5
#define stepPin2 4

#define motor_h_steps 50
#define motor_r_steps 50
#define motor_h_steps_cane 70

#define x_sensorPin 7
#define y_sensorPin 6
#define c_sensorPin 8

void setup() {
  // Declare pins as output:
  pinMode(stepPin1, OUTPUT);
  pinMode(dirPin1, OUTPUT);
  pinMode(stepPin2, OUTPUT);
  pinMode(dirPin2, OUTPUT);
  // pinMode(x_sensorPin, INPUT_PULLUP);
  // pinMode(y_sensorPin, INPUT_PULLUP);
  // pinMode(c_sensorPin, INPUT_PULLUP);
  pinMode(x_sensorPin, INPUT);
  pinMode(y_sensorPin, INPUT);
  pinMode(c_sensorPin, INPUT);
  // Set the spinning direction clockwise:
  digitalWrite(dirPin2, LOW);
  digitalWrite(dirPin1, LOW);
  Serial.begin(9600);
  Serial.println("Starting...");
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


  if(Serial.available()) {

    in_num = get_serial_input_as_int();
    if (in_num<2){
      int sensorVal1 = digitalRead(y_sensorPin);
      int sensorVal2 = digitalRead(x_sensorPin);
      int sensorVal3 = digitalRead(c_sensorPin);
      
      Serial.print("sensorY is ");
      Serial.println(sensorVal1);
      Serial.print("sensorX is ");
      Serial.println(sensorVal2);
      Serial.print("sensorC is ");
      Serial.println(sensorVal3);      
    }  


    if(in_num == MOVE_FLAG) { move_motor(); }
      else if (in_num == CUT_FLAG) { cut(); }
    delay(10);
  }  
}

void move_motor(){
  Serial.println("move mode");
  digitalWrite(dirPin1, LOW);

  for (int i = 0; i < motor_h_steps; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPin1, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(stepPin1, LOW);
    delayMicroseconds(frequency);
  }
}

void cut(){
  cut_motor();
  // for (int i = 0; i < motor_h_steps_cane; i++) {
  //   digitalWrite(stepPin1, HIGH);
  //   delayMicroseconds(frequency);
  //   digitalWrite(stepPin1, LOW);
  //   delayMicroseconds(frequency);
  // }
  // cut_motor();
}

void cut_motor(){
  Serial.println("cut mode");
  digitalWrite(dirPin2, HIGH);
  for (int i = 0; i < motor_r_steps; i++) {
    digitalWrite(stepPin2, HIGH);
    delayMicroseconds(frequency);
    digitalWrite(stepPin2, LOW);
    delayMicroseconds(frequency);
  }
  // digitalWrite(dirPin2, LOW);
  // for (int i = 0; i < motor_r_steps; i++) {
  //   digitalWrite(stepPin2, HIGH);
  //   delayMicroseconds(frequency);
  //   digitalWrite(stepPin2, LOW);
  //   delayMicroseconds(frequency);
  // }
}