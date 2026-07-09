from ai import ask_ai

print("🚀 AI STARTUP")
print("")

prompt = input("Введите тему: ")

answer = ask_ai(prompt)

print("\n==============================")
print("ОТВЕТ ИИ")
print("==============================\n")

print(answer)