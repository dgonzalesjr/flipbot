from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

# Load your API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up LangChain LLM
llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    openai_api_key=openai_api_key
)

# Define prompt template for parsing listings
prompt = ChatPromptTemplate.from_template("""
You are an expert in Pokémon card trading. Given a raw marketplace listing 
title and price, extract and normalize the card information.

Input:
"{listing}"

Output as JSON:
- card_name (string)
- set (string, if known)
- edition (e.g., "1st Edition", "Unlimited", "Unknown")
- holo (true/false)
- condition (e.g., "Near Mint", "Played", "Unknown")
- price (float in USD)
""")

# Define LangChain parsing chain
parse_card_listing_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True
)


# Function to use in your pipeline
def parse_listing(listing_text):
    return parse_card_listing_chain.run(listing=listing_text)


# Test it
if __name__ == "__main__":
    test_listing = "Dark Charizard 1st Edition Holo Near Mint - $120"
    result = parse_listing(test_listing)
    print("\n✅ Parsed result:")
    print(result)
