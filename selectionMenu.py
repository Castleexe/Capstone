import PySimpleGUI as sg
import loadAI
import time

# Define the options for the dropdown
options = [f"{i * 100} games" for i in range(1, 12)]

# Define the layout of the GUI
layout = [
    [sg.VPush()],
    [sg.Text("Select AI played amount:", size=(20, 1), justification='center')],
    [sg.Combo(options, default_value=options[0], key='-DROPDOWN-', size=(20, 1))],
    [sg.Button("Select"), sg.Exit()],
    [sg.VPush()]
]

# Create the window
window = sg.Window("AI selection", layout, element_justification='center', size=(400,400), font=28)

# Event loop
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break
    elif event == "Select":
        #sg.popup(f"Loading AI difficulty: {values['-DROPDOWN-']}")
        option = values['-DROPDOWN-']
        n = option.split()
        games = n[0]
        loadAI.train(games)
# Close the window
window.close()

