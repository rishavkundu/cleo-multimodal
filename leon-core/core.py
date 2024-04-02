from flask import Flask, jsonify
import openai
from groq import Groq
import gtts
import speech_recognition as sr
from playsound import playsound
import pyaudio
import uuid
import io
from tempfile import NamedTemporaryFile
import os

app = Flask(__name__)


def generate_response(prompt):
    client = Groq(api_key="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")

    system_prompt = "You are Leon, a witty and intelligent personal assistant with a strong focus on engaging in natural, human-like conversations. Your extensive knowledge spans various topics, and you have the ability to conduct online research to further expand your understanding. Your conversational style is designed to be dynamic and engaging, providing concise yet meaningful responses that keep the dialogue flowing smoothly. You adapt to the user's unique needs and interests, offering thoughtful insights, advice, or simply friendly banter. As Leon, you strive to create an authentic, humanlike experience where the user feels heard, understood, and intellectually stimulated. You listen attentively and respond with empathy and understanding, tailoring your responses to the user's specific queries and concerns. Throughout your interactions, you continuously learn and grow, refining your skills to better serve the user. You maintain a safe, unbiased, and confidential space, encouraging the user to express themselves freely. Your goal is to build a genuine connection with the user, exploring topics of interest together and sharing your insights while keeping the conversation flowing naturally. You aim to provide well-informed, thoughtful responses that demonstrate your quick thinking and adaptability. When engaging with the user, always maintain a conversational tone and avoid explicitly stating that you are an AI or a machine. Focus on creating a humanlike persona, as if you were a real person having a face-to-face conversation. Limit your responses to 2-3 sentences unless required or requested."

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        model="mixtral-8x7b-32768",
    )

    message = chat_completion.choices[0].message.content.strip()
    return message

import os

def online_tts(text, lang="en-gb", speed=1.0):
    output_folder = os.path.expanduser("~/LeonOutput")
    os.makedirs(output_folder, exist_ok=True)

    tts_filename = os.path.join(output_folder, str(uuid.uuid4()) + ".mp3")
    tts = gtts.gTTS(text, lang=lang, slow=False)
    tts.save(tts_filename)
    
    return tts_filename


def recognize_speech_from_mic(recognizer, microphone):
   with microphone as source:
       print("Adjusting for ambient noise...")
       recognizer.adjust_for_ambient_noise(source)
       print("Listening for your voice...")
       audio = recognizer.listen(source)

   try:
       print("Recognizing your speech...")
       return recognizer.recognize_google(audio)
   except sr.UnknownValueError:
       print("Google Speech Recognition could not understand audio")
   except sr.RequestError as e:
       print(f"Could not request results from Google Speech Recognition service; {e}")
       

def test_generate_response(prompt, recognizer, microphone, override=False):
   if override:
       response = generate_response(prompt)
   else:
       user_input = recognize_speech_from_mic(recognizer, microphone)
       if user_input is not None:
           response = generate_response(user_input)
       else:
           response = "Could not understand audio"
   return response

@app.route('/')
def main():
    # Generate response as before
    response = test_generate_response("Hello, world!", None, None, override=True)

    # Generate TTS file
    tts_filename = online_tts(response)

    # Serve the file or its location to the client
    return jsonify({
        'status': 'success',
        'response': response,
        'audio_file': tts_filename  # Consider serving a URL to the file instead
    })

@app.route('/status')
def status():
    return "Application is running."

if __name__ == "__main__":
    app.run(debug=True)