import pyautogui
import random
import tkinter as tk
import sys
import os

x = 1400
cycle = 0
check = 1
idle_num = [1, 2, 3, 4]
sleep_num = [10, 11, 12, 13, 15]

event_number = random.randrange(1, 3, 1)
impath = os.path.dirname(os.path.abspath(__file__)) + '\\'

dragging = False
mouse_x = 0
mouse_y = 0

# Transfer random no. to event
def event(cycle, check, event_number, x):
    global current_cycle  # Używamy zmiennej globalnej do licznika cykli

    if event_number in idle_num:
        check = 0
        #print('idle')
        window.after(100, update, cycle, check, event_number, x)  # no. 1,2,3,4 = idle
    elif event_number == 5:
        check = 1
        #print('from idle to sleep')
        window.after(100, update, cycle, check, event_number, x)  # no. 5 = idle to sleep
    elif event_number in sleep_num:
        check = 2
        #print('sleep')
        window.after(1000, update, cycle, check, event_number, x)  # no. 10,11,12,13,15 = sleep
    elif event_number == 14:
        check = 3
        #print('from sleep to idle')
        window.after(100, update, cycle, check, event_number, x)  # no. 15 = sleep to idle

# Making gif work 
def gif_work(cycle, frames, event_number, first_num, last_num):
    if cycle < len(frames) - 1:
        cycle += 1
    else:
        cycle = 0
        event_number = random.randrange(first_num, last_num + 1, 1)
    return cycle, event_number

# Update function to cycle through GIF frames and handle events
def update(cycle, check, event_number, x):
    global current_cycle  # Używamy zmiennej globalnej do licznika cykli

    # idle
    if check == 0:
        frame = idle[cycle]
        cycle, event_number = gif_work(cycle, idle, event_number, 1, 5)

    # idle to sleep
    elif check == 1:
        frame = idle_to_sleep[cycle]
        cycle, event_number = gif_work(cycle, idle_to_sleep, event_number, 10, 10)

    # sleep
    elif check == 2:
        frame = sleep[cycle]
        cycle, event_number = gif_work(cycle, sleep, event_number, 10, 15)

    # sleep to idle
    elif check == 3:
        frame = sleep_to_idle[cycle]
        cycle, event_number = gif_work(cycle, sleep_to_idle, event_number, 1, 1)

    # Aktualizujemy okno z nową klatką GIF
    #window.geometry('160x160+' + str(x) + '+1050')
    label.configure(image=frame)

    # Uruchamiamy kolejny cykl animacji
    window.after(1, event, cycle, check, event_number, x)

def load_gifs():
    """Funkcja ładuje wszystkie klatki GIF-ów i przygotowuje je do animacji."""
    try:
        idle = [tk.PhotoImage(file=impath+'idle.gif',format = 'gif -index %i' %(i)) for i in range(15)] # 15 klatek GIF
        idle_to_sleep = [tk.PhotoImage(file=impath+'idle_to_sleep.gif', format='gif -index %i' % i) for i in range(9)]  # 9 klatek GIF
        sleep = [tk.PhotoImage(file=impath+'sleep.gif', format='gif -index %i' % i) for i in range(2)]  # 2 klatki GIF
        sleep_to_idle = [tk.PhotoImage(file=impath+'sleep_to_idle.gif', format='gif -index %i' % i) for i in range(9)]  # 9 klatek GIF
        print("GIF załadowany pomyślnie!")
    except Exception as e:
        print(f"Nie udało się załadować GIF: {e}")
        sys.exit()

    return idle, idle_to_sleep, sleep, sleep_to_idle

def on_mouse_press(event):
    """Rejestrujemy początkową pozycję myszy."""
    global dragging, mouse_x, mouse_y
    dragging = True
    mouse_x, mouse_y = pyautogui.position()

def on_mouse_release(event):
    """Zatrzymujemy śledzenie myszy."""
    global dragging
    dragging = False

def on_mouse_move(event):
    """Przesuwamy okno, jeśli mysz jest wciśnięta."""
    global dragging, mouse_x, mouse_y
    if dragging:
        current_pos = pyautogui.position()
        dx, dy = current_pos.x - mouse_x, current_pos.y - mouse_y
        window.geometry(f'+{window.winfo_x() + dx}+{window.winfo_y() + dy}')
        mouse_x, mouse_y = current_pos.x, current_pos.y

def on_x_press(event):
    global dragging, mouse_x, mouse_y
    if dragging:
        window.quit()
        sys.exit()

window = tk.Tk()

# Załaduj GIF-y przed rozpoczęciem głównej pętli
idle, idle_to_sleep, sleep, sleep_to_idle = load_gifs()

screen_width, screen_height = pyautogui.size()

# Rozmiar okna
window_width = 160  # Szerokość okna (dopasuj do grafiki)
window_height = 160  # Wysokość okna

# Oblicz pozycję w prawym dolnym rogu
x_position = screen_width - window_width
y_position = screen_height - window_height

# Window configuration
window.config(highlightbackground='black')
label = tk.Label(window, bd=0, bg='black')
window.overrideredirect(True)
window.wm_attributes('-topmost', True)
window.wm_attributes('-transparentcolor', 'black')
window.geometry(f'{window_width}x{window_height}+{x_position}+{y_position}')
label.pack()

# Obsługa zdarzeń myszy
window.bind("<Button-1>", on_mouse_press)  # Lewy przycisk myszy
window.bind("<B1-Motion>", on_mouse_move)  # Ruch myszy z wciśniętym przyciskiem
window.bind("<ButtonRelease-1>", on_mouse_release)  # Zwolnienie przycisku myszy
window.bind("<x>", on_x_press)  # X wciśniety

# Start event cycle
window.after(1, update, cycle, check, event_number, x)

window.mainloop()