const int debug_switch = 0; // 0 to test nothing, 1 to test calibration, 2 to test dispensing, 3 to lower cutter blade, 4 to raise cutter blade, 5 to feed mesh forwards, 6 to feed mesh backwards

////  Initialization  ///////////////////////////////////////////////////////////
#include <Stepper.h>

// Digital signal pins to trigger the corresponding method
const int pin_dispense_tab_sequence = 3;
const int pin_calibration_sequence = 2;
int calibration_signal_received = 0;
int dispense_signal_received = 0;

// Define values for the step motors. Transistor pin to prevent wasted power, the steps per revolution, and the rotational speed.
const int circuit_power_transistor_pin = 12;
const int stepsPerRevolution = 2048;
const int rpm = 10;         // Adjustable range of 28BYJ-48 stepper is 0~17 rpm

// Connection pins for the stepper motors to the Arduino.
const int step_motor_extruder_IN1 = 7;
const int step_motor_extruder_IN2 = 6;
const int step_motor_extruder_IN3 = 5;
const int step_motor_extruder_IN4 = 4;
const int step_motor_cutter_IN1 = 11;
const int step_motor_cutter_IN2 = 10;
const int step_motor_cutter_IN3 = 9;
const int step_motor_cutter_IN4 = 8;

// Initialize the stepper motors with the input pins
Stepper step_motor_extruder(stepsPerRevolution, step_motor_extruder_IN4, step_motor_extruder_IN1, step_motor_extruder_IN3, step_motor_extruder_IN2);
Stepper step_motor_cutter(stepsPerRevolution, step_motor_cutter_IN4, step_motor_cutter_IN1, step_motor_cutter_IN3, step_motor_cutter_IN2);

const int phototransistor_1_pin = A0;
const int phototransistor_2_pin = A1;
const int phototransistor_light_threshold = 20;
bool is_light_sensed = false;

const int ROTATION_TO_CUT = 144;
const int ROTATION_TO_FEED = -90;

////  Main loops  ///////////////////////////////////////////////////////////

void setup() {
  // Initialize the components and pins at their appropriate parameter values. Set motor speed and the state of the transistors
  step_motor_extruder.setSpeed(rpm);
  step_motor_cutter.setSpeed(rpm);
  pinMode(circuit_power_transistor_pin, OUTPUT);
  pinMode(pin_calibration_sequence, INPUT);
  pinMode(pin_dispense_tab_sequence, INPUT);
  
  // Make sure that the motors are not on.
  digitalWrite(circuit_power_transistor_pin, LOW);
  
  debug_test();
}

void loop() {
  // Make sure that these pins have a pull-up resistor! If they are not grounded normally these signals will
  // just fire all the time!
  if(digitalRead(pin_calibration_sequence) == HIGH && calibration_signal_received == 0){
    calibration_signal_received = 1;
    calibration_sequence();
  }
  else if(digitalRead(pin_dispense_tab_sequence) == HIGH && dispense_signal_received == 0){
    dispense_signal_received = 1;
    dispense_tab_sequence();
  }
}

////  Sub-functions ///////////////////////////////////////////////////////////

void calibration_sequence(){
  // While the light is detected, continue rotating
  while(check_light_level_versus_threshold(phototransistor_1_pin)){
    rotate_deg(step_motor_extruder, -1, false);
  }
  calibration_signal_received = 0; //Last line
}

void dispense_tab_sequence(){
  // Allows triggering of the tab dispensing sequence by a single digital signal
  rotate_deg(step_motor_extruder, ROTATION_TO_FEED, true); // Dispense a length of mesh
  rotate_deg(step_motor_cutter, ROTATION_TO_CUT, true); // Lower blade
  rotate_deg(step_motor_cutter, -ROTATION_TO_CUT, true); // Raise blade
  dispense_signal_received = 0; //Last line
}

bool check_light_level_versus_threshold(int pin_to_check){
  // Check the analog reading of the given pin; if the reading exceeds the threshold, return "true", there is a light being sensed.
  digitalWrite(circuit_power_transistor_pin, HIGH); // Power circuit
  is_light_sensed = analogRead(pin_to_check) > phototransistor_light_threshold;
  digitalWrite(circuit_power_transistor_pin, LOW); // Unpower circuit
  return is_light_sensed; 
}

void rotate_deg(Stepper stp, int rotateBy, bool also_delay){
  // Allow rotation of the given motor by degrees rather than steps; easier use.
  digitalWrite(circuit_power_transistor_pin, HIGH); // Power circuit
  stp.step(int(double(rotateBy)*double(stepsPerRevolution)/360));
  digitalWrite(circuit_power_transistor_pin, LOW); // Unpower circuit
  if(also_delay){ delay(50); }
}

void debug_test(){
  if(debug_switch == 1){ calibration_sequence(); }
  else if(debug_switch == 2){ dispense_tab_sequence(); }
  else if(debug_switch == 3){ rotate_deg(step_motor_cutter, ROTATION_TO_CUT, true); }
  else if(debug_switch == 4){ rotate_deg(step_motor_cutter, -ROTATION_TO_CUT, true); }
  else if(debug_switch == 5){ rotate_deg(step_motor_extruder, ROTATION_TO_FEED, true); }
  else if(debug_switch == 6){ rotate_deg(step_motor_extruder, -ROTATION_TO_FEED, true); }
}

////  EoF ///////////////////////////////////////////////////////////
