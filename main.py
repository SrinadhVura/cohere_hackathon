import os
import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_CLIENT = os.environ.get("COHERE_CLIENT")
COHERE_MODEL = os.environ.get("COHERE_MODEL")

# print(COHERE_CLIENT)
# print(COHERE_MODEL)
