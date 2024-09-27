import os
import specialsitsai as ssai

if __name__ == "__main__":

    html_folder = "/Users/ignaciomoyaredondo/OneDrive/obsidian/01_projects/secedgarspecial/db_oddlots/html"
    
    # Parse the HTML files
    html_files = ssai.HTMLHandler(html_folder).process_html_files()
    html_file = [file for file in html_files if "MNST" in file["source"]]

    # Set up the RAG system
    #print(ssai.RAGSystem(html_file, use_local=False).retrieve_oddlot_from_docs())
    #print(ssai.RAGSystem(html_file, use_local=False).ask_from_docs(
    #    "Summarize in 300 words maximum the odd lot file including company name, purchase prices and expiry date")
    #)
    print(ssai.RAGSystem(html_file, use_local=False).oddlot_from_docs())