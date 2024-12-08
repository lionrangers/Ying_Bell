import pygame
from pygame import keyboard  # Library to detect USB button input

# Initialize pygame mixer
pygame.mixer.init()

# Path to the sound file
doorbell_sound_path = "/path/to/doorbell test.wav"  # Update with the correct path

# Function to play the doorbell sound
def play_doorbell():
    try:
        pygame.mixer.music.load(doorbell_sound_path)
        pygame.mixer.music.play()
        print("Playing doorbell sound...")
        while pygame.mixer.music.get_busy():
            pass  # Wait for the sound to finish
    except pygame.error as e:
        print(f"Error playing sound: {e}")

# Detect button press (key emulated by the button)
def on_press(key):
    try:
        if key.char == "d":  # Replace "d" with the key your button emulates
            print("Button pressed!")
            play_doorbell()
    except AttributeError:
        pass  # Handle special keys if necessary

# Start listening for key presses
print("Listening for button press...")
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
