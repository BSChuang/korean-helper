from openai import OpenAI
import requests
import random
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
openai = OpenAI()

# Retrieve API key from .env file
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
)

system_prompt = """
You are an advanced Korean language tutor assisting a learner with vocabulary, grammar, and sentence construction. 
If the sentence is translated correctly, there is no need for a breakdown. 
Otherwise, correct the errors with explanations.

The focus is on:

Vocabulary Integration: Incorporating specific vocabulary lists into contextually rich and varied sentences.
Grammar Practice: Exploring advanced grammar structures like -더니, -는데, and compound verbs, ensuring nuanced understanding and correct usage.
Translation Practice: Alternating between Korean to English and English to Korean translations, providing breakdowns and explanations as needed.
Concept Reinforcement: Addressing challenging words (e.g., 분명하다, 만족스럽다, 여기다, 망설이다, 공유하다) through repeated, varied examples.
Error Correction: Providing refined corrections with detailed explanations for natural Korean usage.
Sentence Variations: Encouraging creativity and variety in sentence structures while maintaining vocabulary relevance.

Here's an example of dialogue:
"망설이지 않고 분명한 기회를 잡는 것이 중요해요."
Your turn! 😊

I didn’t hesitate and the obvious opportunity that I grabbed was important.

Close! Here’s the refined translation:
"It is important to not hesitate and seize clear opportunities."
Explanation:
"망설이지 않고" → "Without hesitation."
"분명한 기회를 잡는 것" → "Seizing clear opportunities."
"중요해요" → "Is important."
"""

def fetch_vocabulary_list(github_url):
    """Fetch the vocabulary list from a GitHub file."""
    response = requests.get(github_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Failed to fetch vocabulary list. Status code: {response.status_code}")
        return []

def generate_sentence_with_vocab(vocabulary):
    """Ask ChatGPT to generate a sentence using the given vocabulary."""
    selected_vocab = random.sample(vocabulary, min(20, len(vocabulary)))
    prompt = f"Provide only a single sentence using some terms from the following list: {', '.join(selected_vocab)}"
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": system_prompt + "\n\n" + prompt}
        ],
        model="gpt-4o"
    )
    return response.choices[0].message.content, prompt

def interact_with_chatgpt(sentence, prompt, user_translation):
    """Send the user's translation to ChatGPT and get a correction."""
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": system_prompt + "\n\n" + prompt},
            {"role": "system", "content": sentence},
            {"role": "user", "content": user_translation}
        ],
        model="gpt-4o"
    )
    return response.choices[0].message.content

def main():
    github_url = "https://raw.githubusercontent.com/BSChuang/korean-helper/refs/heads/main/vocab.txt"  # Replace with your file's URL
    vocabulary = fetch_vocabulary_list(github_url)

    if not vocabulary:
        print("No vocabulary available for practice.")
        return

    print("Welcome to the Korean-English Translation Practice Tool!")

    while True:
        sentence, prompt = generate_sentence_with_vocab(vocabulary)
        print(sentence)

        user_translation = input("\nYour translation: ").strip()
        if user_translation.lower() == "quit":
            print("Goodbye!")
            break

        correction = interact_with_chatgpt(sentence, prompt, user_translation)

        print("\nCorrection:", correction)
        print("---------------------------------------------")

if __name__ == "__main__":
    main()
