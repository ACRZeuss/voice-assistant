import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
from diffusers import StableDiffusionPipeline
import torch

# Sesli cevap için motoru başlat
engine = pyttsx3.init()
engine.setProperty("rate", 120)  # Konuşma hızı
engine.setProperty("voice", "tr")  # Türkçe ses (Sisteminiz destekliyorsa)

def speak(text):
    print("Göktürk:", text)
    engine.say(text)
    engine.runAndWait()

# Wikipedia dili Türkçe
wikipedia.set_lang("tr")

pipe = StableDiffusionPipeline.from_pretrained(
    "CompVis/stable-diffusion-v1-4",
    torch_dtype=torch.float32,
)
pipe.to("cuda") # GPU kullanımı için "cuda" veya CPU için "cpu" yazabilirsiniz.

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
        
def generate_image(prompt, filename="output.png"):
    print(f"'{prompt}' komutuna göre görsel üretiliyor...")
    image = pipe(prompt).images[0]
    image.save(filename)
    print(f"'{filename}' olarak kaydedildi.")

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
    
    elif "resim çiz" in command or "çiz" in command:
        speak("Nasıl bir resim çizmemi istersiniz?")
        prompt = listen(timeout=10)
        if prompt:
            speak(f"{prompt} çiziliyor.")
            generate_image(prompt)
            speak("Resim kaydedildi.")
        else:
            speak("Komutu anlayamadım.")
                
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
    WAKE_WORD = "göktürk"

    speak("Göktürk başlatıldı. 'Hey göktürk' diyerek aktif edebilirsiniz.")

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