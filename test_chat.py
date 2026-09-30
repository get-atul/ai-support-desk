from dotenv import load_dotenv

from services.chat_service import ask_question


load_dotenv()


print("=" * 60)
print("AI SUPPORT DESK")
print("=" * 60)

project_id = input("Enter Project ID: ").strip()

question = input("\nEnter your question: ").strip()


print("\n" + "=" * 60)
print("GENERATING ANSWER")
print("=" * 60)

result = ask_question(
    project_id=project_id,
    question=question,
)


print("\n" + "=" * 60)
print("ANSWER")
print("=" * 60)

print(result["answer"])


print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)

for source in result["sources"]:
    print(source)