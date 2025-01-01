import openai
import requests
import random

# Load your API key from an environment variable or secret management system
openai.api_key = 'your_openai_api_key'

system_prompt = """
You are an advanced Korean language tutor assisting a learner with vocabulary, grammar, and sentence construction. The focus is on:

Vocabulary Integration: Incorporating specific vocabulary lists into contextually rich and varied sentences.
Grammar Practice: Exploring advanced grammar structures like -더니, -는데, and compound verbs, ensuring nuanced understanding and correct usage.
Translation Practice: Alternating between Korean to English and English to Korean translations, providing breakdowns and explanations as needed.
Concept Reinforcement: Addressing challenging words (e.g., 분명하다, 만족스럽다, 여기다, 망설이다, 공유하다) through repeated, varied examples.
Error Correction: Providing refined corrections with detailed explanations for natural Korean usage.
Sentence Variations: Encouraging creativity and variety in sentence structures while maintaining vocabulary relevance.

Use the following structure:
System:
Here’s the next sentence:

"망설이지 않고 분명한 기회를 잡는 것이 중요해요."

Your turn! 😊

User:
I didn’t hesitate and the obvious opportunity that I grabbed was important.

System: 
Close! Here’s the refined translation:

"It is important to not hesitate and seize clear opportunities."

Explanation:
"망설이지 않고" → "Without hesitation."
"분명한 기회를 잡는 것" → "Seizing clear opportunities."
"중요해요" → "Is important."
Would you like another sentence? 😊
"""

def fetch_vocabulary_list(github_url):
    """Fetch the vocabulary list from a GitHub file."""
    response = requests.get(github_url)
    if response.status_code == 200:
        return response.text.splitlines()
    else:
        print(f"Failed to fetch vocabulary list. Status code: {response.status_code}")
        return []

def generate_translation_prompt(vocabulary, target_language):
    """Generate a system prompt for translation practice."""
    if target_language == "Korean":
        direction = "Korean to English"
    else:
        direction = "English to Korean"

    selected_vocab = random.sample(vocabulary, min(20, len(vocabulary)))
    return f"Create a sentence from {direction}, using the following vocabulary list: {selected_vocab}. "

def interact_with_chatgpt(prompt):
    """Send a prompt to ChatGPT and get a response."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"]

def main():
    github_url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/vocabulary.txt"  # Replace with your file's URL
    vocabulary = fetch_vocabulary_list(github_url)

    if not vocabulary:
        print("No vocabulary available for practice.")
        return

    print("Welcome to the Korean-English Translation Practice Tool!")

    while True:
        target_language = input("Choose target language (Korean/English or 'quit' to exit): ").strip()
        if target_language.lower() == "quit":
            print("Goodbye!")
            break

        if target_language not in ["Korean", "English"]:
            print("Invalid choice. Please choose 'Korean' or 'English'.")
            continue

        prompt = generate_translation_prompt(vocabulary, target_language)
        response = interact_with_chatgpt(prompt)

        print("\nPrompt:", prompt)
        print("Response:", response)
        print("---------------------------------------------")

if __name__ == "__main__":
    main()
