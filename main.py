from dotenv import load_dotenv
from graph.graph import app

load_dotenv()

if __name__ == "__main__":
    result = app.invoke(input={"question": "Python'da iki sayı nasıl toplanır?"})
    print("\n--- CEVAP ---\n")
    print(result.get("generation", "(generation alanı boş)"))