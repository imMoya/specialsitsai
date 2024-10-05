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
from pydantic import BaseModel, Field, field_validator
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional, Union
from dotenv import load_dotenv


class OddLot(BaseModel):
    #lower_price: Optional[str] = Field(description="What is the lowest price in dollars (or other currency) that the company offers to pay per share in this odd-lot tender offer?")
    lower_price: str = Field(description="The currency in which the minimum purchase price per share is denominated.")
    higher_price: str = Field(description="What is the highest price in dollars (or other currency) that the company offers to pay per share in this odd-lot tender offer?")
    #higher_price_currency: str = Field(description="The currency in which the maximum purchase price per share is denominated.")
    #shares_sought: str = Field(description="The total number of shares the company seeks to purchase.")
    expiration_date: str = Field(description="The deadline for the odd-lot tender offer. Format it as YYYY-MM-DD")
    #payment_terms: str = Field(description="Terms regarding how payment will be made for the purchased shares.")
    #withdrawal_rights: str = Field(description="Information about the right of shareholders to withdraw their tendered shares and the associated deadline.")
    #tax_consequences: str = Field(description="Description of any potential tax implications for shareholders participating in the offer.")
    #method_of_tendering: str = Field(description="Instructions on how to properly tender shares in the offer.")
    #proration: str = Field(description="Indicates whether proration will apply if more shares are tendered than the company is willing to purchase.")
    #financing_conditions: str = Field(description="Details about how the tender offer is financed or whether there are specific financing conditions.")
    #regulatory_approvals: str = Field(description="List any necessary regulatory approvals or clearances that must be obtained before the tender offer can be completed.")
    #factors_affecting_pricing: str = Field(description="A description of factors that the company considered when setting the purchase price range.")
    #shareholder_requirements: str = Field(description="Requirements a shareholder must meet to qualify as an odd-lot holder (e.g., holding fewer than 100 shares).")
    #oddlot_priority: str = Field(description="A statement indicating whether odd-lot holders are given priority in the tender offer, formatter as True or False")
    #risks: str = Field(description="Identify any conditions or contingencies mentioned in the tender offer that could result in its cancellation. Please, expand in the explanation")

    #@field_validator('lower_price', 'higher_price', mode='before')
    #def check_price(cls, v):
    #    # Check if the value is a valid number, otherwise return None
    #    if v is None or not v.replace('.', '', 1).isdigit():  # Allow for decimal numbers
    #        return None
    #    return vX

class OddLotExtractor:
    """Handles asking isolated questions for each OddLot field and aggregates the results."""
    def __init__(self, retriever, llm):
        self.retriever = retriever
        self.llm = llm
        self.fields = [
            # Only fields that you want to extract
            'expiration_date',
            # Uncomment and add more fields as needed
            'lower_price',
            'higher_price',
            #'shares_sought',
            #'payment_terms',
            #'withdrawal_rights',
            #'tax_consequences',
            #'method_of_tendering',
            #'proration',
            #'financing_conditions',
            #'regulatory_approvals',
            #'factors_affecting_pricing',
            #'shareholder_requirements',
            #'oddlot_priority',
            #'risks',
        ]

    def extract_oddlot_info(self) -> OddLot:
        """Extract OddLot info by asking isolated questions for each field."""
        responses = {}

        for field in self.fields:
            prompt = self.get_field_prompt(field)
            retrieved_docs = self.retriever.invoke(prompt)
            combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
            response = self.rag_invoke(prompt, combined_content)
            print(response)
            responses[field] = response

        return responses

    def get_field_prompt(self, field: str) -> str:
        """Generate a prompt for each OddLot field."""
        field_prompts = {
            "expiration_date": "What is the deadline for the odd-lot tender offer? Provide the date in the format YYYY-MM-DD.",
            # Add other field-specific prompts here
            "lower_price": "What is the lowest price offered in the odd-lot tender offer?",
            "higher_price": "What is the highest price offered in the odd-lot tender offer?",
        }
        return field_prompts[field]

    def rag_invoke(self, prompt: str, content: str) -> str:
        """Invoke the RAG system to retrieve information for a specific question."""
        prompt_template = PromptTemplate(
            template="""
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question.
            If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
            Question: {prompt}
            Context: {content}
            Answer:""",
            input_variables=["prompt", "content"]
        )

        formatted_prompt = prompt_template.format_prompt(prompt=prompt, content=content)
        return self.llm(formatted_prompt)  # Invoke the LLM with the formatted prompt

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
        else:
            raise ValueError(f"Unsupported prompt type: {self.type}")

    def get_prompt(self):
        """Returns the appropriate prompt based on the type."""
        if self.type == "ODDLOT":
            return self.define_oddlot_prompt(self.parser)
        elif self.type == "ASK":
            return self.define_general_prompt()
        else:
            raise ValueError(f"Unsupported prompt type: {self.type}")

    @staticmethod
    def define_oddlot_prompt(parser_: PydanticOutputParser) -> PromptTemplate:
        """Defines a prompt template for OddLot extraction."""
        format_instructions = parser_.get_format_instructions()
        return PromptTemplate(
            template="""
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
            If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise. Format as needed when specified in the questions
            Questions: {format_instructions}
            Context: {file}
            Answers:""",
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
        self._vectorstore = None
        self._retriever = None
        load_dotenv()

    @property
    def documents(self):
        with ThreadPoolExecutor() as executor:
            documents = list(executor.map(self.create_document_from_file, self.html_files))
            documents = [doc for sublist in documents for doc in sublist]
        return documents
    
    @staticmethod
    def create_document_from_file(file):
        return [Document(metadata={"source": file["source"]}, page_content=file["page_content"])]
    
    @property
    def vectorstore(self):
        """Lazily create the vector store and cache the result."""
        if not self._vectorstore:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
            splits = text_splitter.split_documents(self.documents)
            self._vectorstore = Chroma.from_documents(documents=splits, embedding=self.get_embedding_model())
        return self._vectorstore
  
    def get_embedding_model(self):
        """Select the embedding model based on the configuration."""
        if self.use_local:
            return OllamaEmbeddings(model="llama3")  # Example local model
        else:
            openai_api_key = os.getenv("OPENAI_API_KEY")
            return OpenAIEmbeddings(openai_api_key=openai_api_key)  # Example OpenAI model

    @property
    def retriever(self):
        """Lazily set up the retriever."""
        if not self._retriever:
            self._retriever = self.vectorstore.as_retriever()
        return self._retriever

    @property
    def llm(self):
        return self.get_llm()
    
    def get_llm(self):
        """Select the language model based on the configuration."""
        if self.use_local:
            return Ollama(model="llama3")  
        return ChatOpenAI(model="gpt-4o-mini")

    def rag_invoke(self, prompt_type: str, content: dict):
        """General method for retrieving information based on prompt type."""
        pm = PromptManager(type=prompt_type)
        rag_chain = pm.prompt | self.llm | pm.parser
        return rag_chain.invoke(content)
    
    def oddlot_from_fulldocs(self):
        """Retrieve OddLot information from full documents."""
        combined_content = "\n\n".join(doc.page_content for doc in self.documents)
        return self.rag_invoke(prompt_type="ODDLOT", content={"file": combined_content})
    
    def oddlot_from_docs(self):
        """Retrieve OddLot information from retrieved documents."""
        retrieved_docs = self.retriever.invoke(PromptManager(type="ODDLOT").parser.get_format_instructions())
        combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return self.rag_invoke(prompt_type="ODDLOT", content={"file": combined_content})
    
    def oddlot_from_docs_isolated(self):
        """Retrieve OddLot information by asking isolated questions for each field."""
        oddlot_extractor = OddLotExtractor(self.retriever, self.llm)
        return oddlot_extractor.extract_oddlot_info()

    
    def ask_from_docs(self, query):
        """Perform a query using a general RAG prompt."""
        retrieved_docs = self.retriever.invoke(query)
        combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
        return self.rag_invoke(prompt_type="ASK", content={"context": combined_content, "question": query})
    