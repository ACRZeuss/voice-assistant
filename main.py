import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser

# Sesli cevap için motoru başlat
engine = pyttsx3.init()
engine.setProperty("rate", 120)  # Konuşma hızı
engine.setProperty("voice", "tr")  # Türkçe ses (Sisteminiz destekliyorsa)

def speak(text):
    print("Asistan:", text)
    engine.say(text)
    engine.runAndWait()

# Wikipedia dili Türkçe
wikipedia.set_lang("tr")

# Mikrofondan ses al (timeout ile)
def listen(timeout=None):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Komut bekleniyor...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, timeout=timeout)
            command = r.recognize_google(audio, language="tr-TR")
            print("Komut alındı:", command)
            return command.lower()
        except sr.WaitTimeoutError:
            print("Komut süresi doldu.")
            return ""
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
        
    # elif "arama yap" in command:
    #     speak("Ne aramak istiyorsunuz?")
    #     query = listen()
    #     if query:
    #         try:
    #             summary = wikipedia.summary(query, sentences=2)
    #             print("Bilgi:", summary)
    #             speak(summary)
    #         except:
    #             speak("Bu konuda bir şey bulamadım.")
                
    elif "youtube'da ara" in command or "youtube'da bak" in command:
        speak("YouTube'da ne aramak istersiniz?")
        query = listen(timeout=10)
        if query:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            speak(f"YouTube'da {query} için sonuçlar getiriliyor.")
            webbrowser.open(url)
            
    elif "kapat" in command or "görüşürüz" in command:
        speak("Görüşmek üzere!")
        exit()
    else:
        speak("Bu komutu bilmiyorum.")

# Ana döngü
if __name__ == "__main__":
    WAKE_WORD = "hey asistan"

    speak("Asistan başlatıldı. 'Hey asistan' diyerek aktif edebilirsiniz.")

    while True:
        print("Wake-word bekleniyor...")
        heard = listen()
        if WAKE_WORD in heard:
            speak("Evet, sizi dinliyorum.")
            command = listen()
            if command:
                process_command(command)
        else:
            print("Wake-word algılanmadı.")