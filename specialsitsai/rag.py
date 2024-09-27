import os
import logging
from concurrent.futures import ThreadPoolExecutor
from langchain import hub
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts.prompt import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_community.llms import Ollama
from pydantic import BaseModel, Field
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional, Union
from dotenv import load_dotenv

class OddLot(BaseModel):
    lower_price: str = Field(description="The minimum purchase price per share of the odd-lot tender offer.")
    lower_price_currency: str = Field(description="The currency of the minimum purchase price per share of the odd-lot tender offer.")
    higher_price: str = Field(description="The maximum purchase price per share of the odd-lot tender offer.")
    higher_price_currency: str = Field(description="The currency of the maximum purchase price per share of the odd-lot tender offer.")
    expiration_date: str = Field(description="The date the odd-lot tender offer expires (formatted as YYYY-MM-DD).")

class PromptManager:
    """Handles different types of prompt templates."""
    def __init__(self, type: Optional[str]=None):
        self.type = type

    @property
    def prompt(self):
        return self.get_prompt()
    
    @property
    def parser(self):
        return self.get_parser()

    def get_parser(self) -> Union[PydanticOutputParser, StrOutputParser]:
        if self.type == "ODDLOT":
            return PydanticOutputParser(pydantic_object=OddLot)
        elif self.type == "ASK":
            return StrOutputParser()

    def get_prompt(self):
        """Returns the appropriate prompt based on the type."""
        if self.type == "ODDLOT":
            return self.define_odd_lot_prompt()
        elif self.type == "ASK":
            return self.define_general_prompt()
        else:
            raise ValueError(f"Unsupported prompt type: {self.type}")

    @staticmethod
    def define_odd_lot_prompt(parser_: PydanticOutputParser) -> PromptTemplate:
        """Defines a prompt template for OddLot extraction."""
        format_instructions = parser_.get_format_instructions()
        return PromptTemplate(
            template="Please extract the following information from the file provided"
            "\n\n{format_instructions}\n\n{file}",
            input_variables=["file"],
            partial_variables={"format_instructions": format_instructions},
        )

    @staticmethod
    def define_general_prompt():
        """Pulls a general RAG prompt from the hub."""
        return hub.pull("rlm/rag-prompt") 


class RAGSystem:
    def __init__(self, html_files: List[dict], use_local: bool = True):
        self.html_files = html_files
        self.use_local = use_local
        self.chunks = []
        load_dotenv()

    @property
    def documents(self):
        with ThreadPoolExecutor() as executor:
            documents = list(executor.map(self.create_document_from_file, self.html_files))
            documents = [doc for sublist in documents for doc in sublist]
        return documents
    
    @property
    def vectorstore(self):
        return self.create_vector_store()
    
    @property
    def prompt(self, type="ODDLOT"):
        if type == "ODDLOT":
            return self.define_odd_lot_prompt()
    
    @property
    def retriever(self):
        return self.setup_retriever()

    @property
    def llm(self):
        return self.get_llm()
    
    @property
    def rag_chain(self):
        return self.setup_rag_chain()
    
    @property
    def parser(self):
        return PydanticOutputParser(pydantic_object=OddLot)
    
    @staticmethod
    def create_document_from_file(file):
        return [Document(metadata={"source": file["source"]}, page_content=file["page_content"])]
    
    def define_odd_lot_prompt(self):
        parser = self.parser
        format_instructions = parser.get_format_instructions()
        prompt = PromptTemplate(
            template="Please extract the following information from the file provided"
            "\n\n{format_instructions}\n\n{html_file}",
            input_variables=["html_file"],
            partial_variables={"format_instructions": format_instructions},
        )
        return prompt
    
    def get_embedding_model(self):
        """Select the embedding model based on the configuration."""
        if self.use_local:
            return OllamaEmbeddings(model="llama3")  # Example local model
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            return OpenAIEmbeddings(openai_api_key=openai_api_key)  # Example OpenAI model
        
    def create_vector_store(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
        splits = text_splitter.split_documents(self.documents)
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.get_embedding_model())
        return vectorstore
    
    def setup_retriever(self):
        """Set up the retriever using the vector store."""
        return self.vectorstore.as_retriever()
    
    def get_llm(self):
        """Select the language model based on the configuration."""
        if self.use_local:
            return Ollama(model="llama3")  
        else:
            return ChatOpenAI(model="gpt-4o-mini")
    
    def setup_rag_chain(self):
        rag_chain = self.prompt | self.llm | self.parser
        return rag_chain
    
    def retrieve_oddlot_from_single_doc(self):
        combined_content = "\n\n".join(doc.page_content for doc in self.documents)
        return self.rag_chain.invoke({"html_file": combined_content})
    
    def retrieve_oddlot_from_docs(self):
        retrieved_docs = self.retriever.invoke(self.parser.get_format_instructions())
        combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return self.rag_chain.invoke({"html_file": combined_content})
    
    def ask(self, query):
        retrieved_docs = self.retriever.invoke(query)
        combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        pm = PromptManager(type="ASK")
        rag_chain = pm.prompt | self.llm | pm.parser
        return rag_chain.invoke({"context": combined_content, "question": query})
        
    