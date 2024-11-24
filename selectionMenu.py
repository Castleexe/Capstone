import PySimpleGUI as sg
import loadAI

# Define the options for the dropdown
options = [f"{i * 100} games" for i in range(1, 12)]

# Define the layout of the GUI
layout = [
    [sg.Text("Select AI version:", size=(20, 1), justification='center')],
    [sg.Combo(options, default_value=options[0], key='-DROPDOWN-', size=(20, 1))],
    [sg.Button("Select"), sg.Exit()]
]

# Create the window
window = sg.Window("AI selection", layout, element_justification='center')

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

def showScores(humanScore, Aiscore):
    if humanScore > Aiscore:
        sg.popup(f"Your score: {humanScore}, AI score {Aiscore} \n You Win! ")
    else: 
        sg.popup(f"Your score: {humanScore}, AI score {Aiscore} \n Ai Wins :( ")
    
    