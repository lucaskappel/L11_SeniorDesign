# Tkinter is a GUI programming toolkit for python. It is used to create a simple user input box for
# the coating parameters. 
import tkinter as tk


# Variables for the displaying of information on the GUI. Took out control over speed and valve_time because there's no reason to ever change that.
form_fields = ["Home Position - X","Home Position - Y","Column Spacing", "Row Spacing", "Count - Rows","Count - Columns", "Number of Surfaces"] #"Valve Time","Speed"
form_fields_initial_values = [11, -295.5, 29.464, 32.004, 9, 12, 108] # 0.5, 3000,
form_fields_units = ["mm", "mm", "mm", "mm", "#", "#", "#"]

# TODOs, signals and timings for the attachment, currently nothing happens at this step. Select the appropriate
# M-series G-code command and put them in the empty "" below to enable the corresponding features.
calibrate_tab_dispenser_g_code_signal_on = "" #TODO - turn the digital signal to trigger calibration on
calibrate_tab_dispenser_g_code_signal_off = "" #TODO - reset the digital signal to trigger calibration
dispense_tab_g_code_signal_on = "" #TODO - Turn the digital signal to the attachment on to tell it to dispense one tab
dispense_tab_g_code_signal_off = "" #TODO - reset the digital signal to trigger dispensing
dispense_tab_delay_time = 1 #TODO - How long to wait for tab dispension to complete
# Displacement offset for the tab dispensing; the gantry head must be moved from the syringe’s normal position to place the tabs appropriately.
tab_dispenser_x_offset_from_syringe_normal_position = 11 #TODO
tab_dispenser_y_offset_from_syringe_normal_position = 7 #TODO
valve_time_for_tab = 0.1 # TODO – Add a DROP to the tab

    
# Function creating the GUI
def makeform(root, fields, initial_values, units):
    entry_box_dictionary = {}
    for i in range(0, len(fields)):
        this_row = tk.Frame(root)
        row_field = tk.Label(this_row, width=22, text=fields[i], anchor='w')
        row_entry_box = tk.Entry(this_row)
        row_entry_box.insert((0), initial_values[i])
        row_unit = tk.Label(this_row, width=6, text="[" + units[i] + "]", anchor='w')
        
        this_row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        row_field.pack(side=tk.LEFT)
        row_unit.pack(side=tk.RIGHT)
        row_entry_box.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        entry_box_dictionary[fields[i]] = row_entry_box
    return entry_box_dictionary


def pathing_function(spacing_col, spacing_row, valve_time, speed, row_count, col_count, number_of_surfaces, is_for_polymer):
    # Movement commands in G-code form
    dispense = []
    if is_for_polymer == 1:
        dispense = ["M8; open valve \n", "G4 P" + valve_time + "; dwell for "+ valve_time +" seconds \n", "M9; close valve \n"]
    else:
		# ORDER OF OPERATIONS:
		# [ offset to position the tab dispensing 
		# dispense one tab
		# return to default position
		# dispense a tiny amount of polymer to cover the tab]
        dispense = [
		"G91 G1 X" + str(tab_dispenser_x_offset_from_syringe_normal_position) + " Y" + str(tab_dispenser_y_offset_from_syringe_normal_position) + " F" + speed + "; \n",
		dispense_tab_g_code_signal_on + ";\n", " G4 P" + str(dispense_tab_delay_time) + ";\n", dispense_tab_g_code_signal_off + ";\n",
		"G91 G1 X-" + str(tab_dispenser_x_offset_from_syringe_normal_position) + " Y-" + str(tab_dispenser_y_offset_from_syringe_normal_position) + " F" + speed + "; \n",
		"M8; \n", "G4 P" + str(valve_time_for_tab) + ";\n", "M9; \n"]
		
	# Defining some movement commands
    jog_east  = ["G91 G1 X"  + spacing_col + " F" + speed + " \n"]
    jog_west  = ["G91 G1 X-" + spacing_col + " F" + speed + " \n"]
    jog_north = ["G91 G1 Y"  + spacing_row + " F" + speed + " \n"]

     
    g_code_body = []
    surfaces_coated = 0
    for row_index in range(0, row_count):
        
        # If all the surfaces have been coated, break the sequence.
        if surfaces_coated >= number_of_surfaces:
            break
        
        # Check to see if the number of columns or the number of surfaces remaining is smaller
        # Use the smaller one as the number of surfaces to finish in that row
        number_of_surfaces_in_this_row_to_coat = 0
        if (number_of_surfaces - surfaces_coated) > col_count:
            number_of_surfaces_in_this_row_to_coat = col_count - 1
        else:
            number_of_surfaces_in_this_row_to_coat = (number_of_surfaces - surfaces_coated) - 1
        
        # Add that many to the number of surface coated.
        surfaces_coated = surfaces_coated + number_of_surfaces_in_this_row_to_coat + 1
        
        # Coat the row
        if row_index % 2 == 0: # If it's an even row we dispense towards the east, odd dispenses to the west.
            for surface_index in range(0, number_of_surfaces_in_this_row_to_coat):
                g_code_body = g_code_body + dispense + jog_east
        else:
            for surface_index in range(0, number_of_surfaces_in_this_row_to_coat):
                g_code_body = g_code_body + dispense + jog_west
        g_code_body = g_code_body + dispense
        if row_index < row_count - 1:
            g_code_body = g_code_body + jog_north
    return g_code_body


# this function is just creating a text file that is populated with G-Code commands. To see a list of
# G-code commands follow this link -> https://www.reprap.org/wiki/G-code. It just slaps together a bunch
# of strings.
def generateCode(entry_box_dictionary, tabs_or_polymer):
    
    # Get variables from interface
    home_position_x = str(entry_box_dictionary["Home Position - X"].get())
    home_position_y = str(entry_box_dictionary["Home Position - Y"].get())
    spacing_col     = str(entry_box_dictionary["Column Spacing"].get())
    spacing_row     = str(entry_box_dictionary["Row Spacing"].get())
    valve_time = "0.5"  #str(entry_box_dictionary["Valve Time"].get()) # Alternate string if want to let people change this from the interface
    speed      = "3000" #str(entry_box_dictionary["Speed"].get()) # Alternate string if want to let people change this from the interface
    row_count = int(entry_box_dictionary['Count - Rows'].get())
    col_count = int(entry_box_dictionary['Count - Columns'].get())
    number_of_surfaces = int(entry_box_dictionary["Number of Surfaces"].get())
    
    # Create the header and footer of the G-code file
    initial = ["$H \n",
               "G1 G90 G17 G21 G54 F1000;  \n",
               "G10 P0 L20 X0 Y0; set coordinate axis to 0,0 at this point \n",
               "G90 G1 X" + home_position_x + " Y" + home_position_y + " F" + speed + "; bottom left lens \n",
               "G10 P0 L20 X0 Y0; set coordinate axis to 0,0 at this point \n",
			   calibrate_tab_dispenser_g_code_signal_on + "; " + calibrate_tab_dispenser_g_code_signal_on + "; calibrate tab dispenser"]
    final = ["$H \n",]
    go_to_origin = [ "G90 G1 X" + home_position_x + " Y" + home_position_y + " F" + speed + ";\n"]
    
    # Open the GCode file for writing
    GCode_file = open("G_Code.txt","w+")
    
    # Create the body of the G-code for the polymer dispensing
    is_for_polymer = 1
    g_code_body_polymer = pathing_function(spacing_col, spacing_row, valve_time, speed, row_count, col_count, number_of_surfaces, is_for_polymer)
    
    # Create the body of the G-code for the tab dispensing
    is_for_polymer = 0
    g_code_body_tabs    = pathing_function(spacing_col, spacing_row, valve_time, speed, row_count, col_count, number_of_surfaces, is_for_polymer)        
            
    # Write the resulting block of commands to the file and close the file.
    full_command = initial + g_code_body_polymer + go_to_origin + g_code_body_tabs + final
    for g_command in full_command:
        GCode_file.writelines(g_command)
    GCode_file.close()
    

### Main function ###
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Code Generation")
    ents = makeform(root, form_fields, form_fields_initial_values, form_fields_units)
    b1 = tk.Button(root, text='Quit', command=(root.destroy))
    b1.pack(side=tk.RIGHT, padx=5, pady=5)
    b2 = tk.Button(root, text='Generate Code',command=(lambda e=ents: generateCode(e, "polymer")))
    b2.pack(side=tk.RIGHT, padx=5, pady=5)
    root.mainloop()

### EoF ###
