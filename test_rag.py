from dotenv import load_dotenv

load_dotenv()

from core.rag_engine import load_rag_chain, ask_question


print("=" * 60)
print("Loading RAG...")
print("=" * 60)

rag_chain = load_rag_chain()

question = "What was discussed in the meeting?"

answer = ask_question(
    rag_chain,
    question
)

print("\n" + "=" * 60)
print("FINAL ANSWER")
print("=" * 60)
print(answer)