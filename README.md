# L11_SeniorDesign
Senior Design Project Files

"First_Contact_Gantry_GCode_Generator.py" is the python code which generates G-code.
Initial parameters can be modified in any text editor.

#TODOs (machine signals, tuning of delay, offset, valve time)

calibrate_tab_dispenser_g_code_signal_on = "" #TODO - turn the digital signal to trigger calibration on
calibrate_tab_dispenser_g_code_signal_off = "" #TODO - reset the digital signal to trigger calibration
dispense_tab_g_code_signal_on = "" #TODO - Turn the digital signal to the attachment on to tell it to dispense one tab
dispense_tab_g_code_signal_off = "" #TODO - reset the digital signal to trigger dispensing

dispense_tab_delay_time = 1 #TODO - How long to wait for tab dispension to complete
# Displacement offset for the tab dispensing; the gantry head must be moved from the syringe’s normal position to place the tabs appropriately.
tab_dispenser_x_offset_from_syringe_normal_position = 11 #TODO
tab_dispenser_y_offset_from_syringe_normal_position = 7 #TODO
valve_time_for_tab = 0.1 # TODO – Add a DROP to the tab

--------------------------------------------------------------------------------------------------------------------------------------------------

"stepper_core_rev_2.ino" is the arduino code for a correctly wired attachment. Modifications will have to be made to this code if the diagram is not followed, or if I messed something up. But I tested it with my stuff, so I think the code is correct.
//TODOS
Fine tune the following variables:
const int ROTATION_TO_CUT = -144;
const int ROTATION_TO_FEED = -90;

And these two should be fine, but may need some minor adjustment for optimal operation
const int rpm = 10; 
const int phototransistor_light_threshold = 20;


--------------------------------------------------------------------------------------------------------------------------------------------------

"senior_design_first_prototype_arduino_code.ino" is a modified version of the "stepper_core_rev_2.ino" file for the prototype attachment delivered to Dr. Hamilton by L11 Applicaiton Bot Group. It is identical in every way except the pin wiring.
