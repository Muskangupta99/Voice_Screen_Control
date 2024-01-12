import tkinter as tk
from threading import Thread
import speech_recognition as sr
import pyautogui

class VoiceControlledApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice-Controlled Scrolling")
        self.stop_flag = False

        self.init_ui()

    def init_ui(self):
        # Buttons
        self.start_button = tk.Button(self.master, text="Start", command=self.start_listening)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_listening)
        self.stop_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(self.master, text="Waiting for commands...")
        self.status_label.pack(pady=10)

    def start_listening(self):
        self.stop_flag = False
        self.status_label.config(text="Listening for commands...")
        self.listen_thread = Thread(target=self.main_loop_thread)
        self.listen_thread.start()

    def stop_listening(self):
        self.stop_flag = True
        self.status_label.config(text="Stopped listening.")

    def main_loop_thread(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=5)

        while not self.stop_flag:
            try:
                with microphone as source:
                    audio = recognizer.listen(source)
                print("Audio recorded:", audio)

                if audio:
                    command = recognizer.recognize_google(audio).lower()
                    print("Recognized Command:", command)

                    if "up" in command:
                        if "little" in command:
                            self.scroll_up(amount=200)
                        else:
                            self.scroll_up()
                    elif "down" in command:
                        if "little" in command:
                            self.scroll_down(amount=200)
                        else:
                            self.scroll_down()
                    elif "zoom in" in command:
                        self.zoom_in()
                    elif "zoom out" in command:
                        self.zoom_out()

            except sr.UnknownValueError:
                print("Speech Recognition could not understand the audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

    def scroll_up(self, amount=500):
        pyautogui.scroll(amount)

    def scroll_down(self, amount=500):
        pyautogui.scroll(-amount)

    def zoom_in(self):
        pyautogui.hotkey('ctrl', '+')

    def zoom_out(self):
        pyautogui.hotkey('ctrl', '-')

def main():
    root = tk.Tk()
    app = VoiceControlledApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
