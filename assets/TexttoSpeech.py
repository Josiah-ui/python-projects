from gtts import gTTS

text = "Hello, this is a text to speech conversion example."
# Create a gTTS object          
tts = gTTS(text=text, lang='en')
# Save the audio file
tts.save("output.mp3")

print("Text to speech conversion completed. The audio file is saved as 'output.mp3'.")