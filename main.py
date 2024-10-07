import os
import specialsitsai as ssai

if __name__ == "__main__":

    oddlot_folder = "/Users/ignaciomoyaredondo/OneDrive/obsidian/01_projects/secedgarspecial/db_oddlots/html"
    
    # Parse the HTML files
    html_files = ssai.HTMLHandler(oddlot_folder).process_html_files()
    #html_file = [file for file in html_files if "MNST" in file["source"]]
    html_file = [file for file in html_files if "MNST" in file["source"]]
    #MSCF not reading well
    

    # Set up the RAG system
    rag = ssai.RAGSystem(html_file, use_local=False, embedding_context=False)
    print(rag.query_oddlot_details())
    #chatbot = ssai.Chatbot(rag)
    #chatbot.start_chat()

    #spinoff_folder = "/Users/ignaciomoyaredondo/OneDrive/obsidian/01_projects/secedgarspecial/db_spinoffs/html"
    #html_files = ssai.HTMLHandler(spinoff_folder).process_html_files()
    #html_file = [file for file in html_files if "SEG" in file["source"]]
    #print(html_file)

    #print(ssai.RAGSystem(html_file, use_local=False).ask_from_docs(
    #    "Tell me the basic information of the spinoff (parent company and spinoff company) and other financial relevant information in no more than 400 words")
    #)