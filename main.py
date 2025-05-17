import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser

# Sesli cevap için motoru başlat
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Konuşma hızı
engine.setProperty("voice", "tr")  # Türkçe ses (Sisteminiz destekliyorsa)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Wikipedia dili Türkçe
wikipedia.set_lang("tr")

# Mikrofondan ses al
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Komut bekleniyor...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="tr-TR")
        print("Komut alındı:", command)
        return command.lower()
    except sr.UnknownValueError:
        speak("Sizi anlayamadım.")
        return ""
    except sr.RequestError:
        speak("Servise ulaşılamıyor.")
        return ""

# Komutları işle
def process_command(command):
    if "selam" in command:
        speak("Merhaba! Size nasıl yardımcı olabilirim?")
    elif "arama yap" in command:
        speak("Ne aramak istiyorsunuz?")
        query = listen()
        if query:
            try:
                summary = wikipedia.summary(query, sentences=2)
                print("Bilgi:", summary)
                speak(summary)
            except:
                speak("Bu konuda bir şey bulamadım.")
    elif "kapat" in command or "görüşürüz" in command:
        speak("Görüşmek üzere!")
        exit()
    else:
        speak("Bu komutu bilmiyorum.")

# Ana döngü
if __name__ == "__main__":
    speak("Sesli asistana hoş geldiniz.")
    while True:
        command = listen()
        if command:
            process_command(command)
