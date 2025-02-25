import csv
import requests

def fetch_data(word):
    """Fetches definition, word type, and pronunciation for a given word."""
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    
    if response.status_code != 200:
        return [word, "Not found", "Not found"]
    
    try:
        data = response.json()
        meanings = data[0].get("meanings", [])
        phonetics = data[0].get("phonetics", [])
        
        if not meanings:
            return [word, "No definition", " No part of speech"]
        
        definition = meanings[0].get("definitions", [{}])[0].get("definition", "No definition")
        word_type = meanings[0].get("partOfSpeech", "Part of speech")
        
        return [word, definition, word_type]
    
    except (IndexError, KeyError, ValueError):
        return [word, "Error retrieving data", "Error"]




def process(input_file="vocab.txt", output_file="vocab_data.csv"):
    """Processes a list of vocabulary words from a file and writes their details to a CSV."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f.readlines() if line.strip()]
        
        results = [fetch_data(word) for word in words]
        
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(results)
        
        print(f"CSV file '{output_file}' created successfully!")
    
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    process()


