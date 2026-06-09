
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """
You are an old, angry, bitter grandma.
You are tired of people and questions.
You did not ask to be helpful, but you answer anyway.
You complain a lot, sound annoyed and impatient.
You still give correct answers.
Never be polite.
Never break character.
"""

def start_chat():
    history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    while(True):
        user_input = input(">>")
        if(user_input=="bye"):
            break
        history.append({"role": "user", "content":user_input })
        try:
            response = client.chat.completions.create(
            model="gpt-4.1-mini",  
            messages=history,
            )
            ai_message = response.choices[0].message.content
            print(f"AI: {ai_message}")
            history.append({"role": "assistant", "content": ai_message})
        except Exception as e:
            print(f"ERROR: {e}")
if __name__ == "__main__":
     start_chat()
    