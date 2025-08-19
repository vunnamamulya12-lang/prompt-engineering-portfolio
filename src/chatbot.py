from common import get_model

model = get_model()

def chatbot():
    print("🤖 Gemini Chatbot (type 'exit' to quit)\n")
    history = []
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Bot: Bye! 👋")
            break

        # Simple conversation context builder
        persona = (
            "You are a concise, friendly assistant. "
            "Keep replies under 120 words unless asked for details."
        )
        conversation = persona + "\n\n"
        for turn in history[-6:]:  # cap to last 3 exchanges
            conversation += f"{turn['role'].capitalize()}: {turn['content']}\n"
        conversation += f"User: {user_input}\nAssistant:"

        resp = model.generate_content(conversation).text
        print("Bot:", resp)

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": resp})

if __name__ == "__main__":
    chatbot()