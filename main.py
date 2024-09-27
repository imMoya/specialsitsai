import os
import specialsitsai as ssai

if __name__ == "__main__":

    html_folder = "/Users/ignaciomoyaredondo/OneDrive/obsidian/01_projects/secedgarspecial/db_oddlots/html"
    
    # Parse the HTML files
    html_files = ssai.HTMLHandler(html_folder).process_html_files()
    print(len(html_files))
    html_file = [file for file in html_files if "MNST" in file["source"]]

    # Question
    question = """
    Extract from the file provided the following and put it in the format defined in brackets". 
    - Lower limit purchase price per share of the odd-lot tender offer (number, currency)
    - Higher limit purchase price per share of the odd-lot tender offer (number, currency)
    - Expiration date of the odd-lot tender offer (date in the format YYYY-MM-DD)
    """
    # Set up the RAG system
    #print(ssai.RAGSystem(html_file, use_local=False).retrieve_oddlot_from_docs())
    print(ssai.RAGSystem(html_file, use_local=False).ask(
        "Summarize in 300 words maximum the odd lot file including company name, purchase prices and expiry date")
    )