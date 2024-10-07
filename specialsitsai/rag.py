import os
from concurrent.futures import ThreadPoolExecutor
from langchain import hub
from langchain_chroma import Chroma
from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import PromptTemplate
from langchain_community.embeddings import OllamaEmbeddings
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langchain_community.llms import Ollama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Optional, Union
from dotenv import load_dotenv

from specialsitsai.oddlots import ODD_LOT_QUESTIONS

class RAGSystem:
    def __init__(self, html_files: List[dict], use_local: bool = True, embedding_context: bool = False):
        self.html_files = html_files
        self.use_local = use_local
        self.embedding_context = embedding_context
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
    
    def generate_chunk_context(self, chunk: str, document_summary: str) -> str:
        """Use an LLM to generate chunk-specific context."""
        prompt_template = PromptTemplate(
            template="""
            Given the following summary of the document:
            {summary}
            
            Please generate a concise context that should be appended to the following chunk:
            {chunk}
            
            Context:""",
            input_variables=["summary", "chunk"]
        )
        prompt = prompt_template.format(summary=document_summary, chunk=chunk)
        return self.llm.invoke(prompt).content

    def create_contextualized_chunks(self, splits: List[Document], document_summary: str) -> List[Document]:
        """Enhance each chunk with LLM-generated context."""
        enhanced_chunks = []
        for split in splits:
            chunk_content = split.page_content
            # Generate context for this chunk using the document summary
            chunk_context = self.generate_chunk_context(chunk_content, document_summary)
            # Append the context to the chunk content
            enhanced_chunk_content = f"{chunk_context}\n\n{chunk_content}"
            enhanced_chunks.append(Document(metadata=split.metadata, page_content=enhanced_chunk_content))
        return enhanced_chunks
    
    def get_document_summary(self, documents: List[Document]) -> str:
        """Use an LLM to generate a summary of the entire document."""
        combined_content = "\n\n".join(doc.page_content for doc in documents)
        prompt_template = PromptTemplate(
            template="""
            Summarize the following document in a concise manner:
            {document}
            
            Summary:""",
            input_variables=["document"]
        )
        prompt = prompt_template.format(document=combined_content)
        return self.llm.invoke(prompt).content
    
    @property
    def vectorstore(self):
        """Lazily create the vector store and cache the result."""
        if not self._vectorstore:
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=300)
            splits = text_splitter.split_documents(self.documents)
            if self.embedding_context == True:
                document_summary = self.get_document_summary(self.documents)
                contextualized_splits = self.create_contextualized_chunks(splits, document_summary)
                self._vectorstore = Chroma.from_documents(documents=contextualized_splits, embedding=self.get_embedding_model())
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

    def rag_invoke(self, 
                   parser: Union[PydanticOutputParser,StrOutputParser, DatetimeOutputParser],
                   content: dict):
        """General method for retrieving information based on prompt type."""
        prompt = PromptTemplate(
            template="""
            You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. 
            Question: \n{format_instructions}\n{query}\n
            Context: {context}
            Answer:""",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        rag_chain = prompt | self.llm | parser
        return rag_chain.invoke(content)
    
    def query_questions(self, questions: dict):
        responses = {}
        for key, question in questions.items():
            parser = question["parser"]
            retrieved_docs = self.retriever.invoke(question["query"])
            combined_content = "\n\n".join(doc.page_content for doc in retrieved_docs)
            responses[key] = self.rag_invoke(parser, {"context": combined_content, "query": question["query"]})
        return responses

    def query_oddlot_details(self, questions=ODD_LOT_QUESTIONS):
        """Method to ask multiple questions about the OddLot tender."""
        return self.query_questions(questions)
