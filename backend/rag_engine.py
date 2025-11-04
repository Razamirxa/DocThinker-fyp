"""
RAG Engine Module
Extracted from academic-rag-assistant-master/app.py
Provides core RAG functionality using LangChain, Pinecone, and Google Gemini
"""

import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime

from langchain.retrievers import MultiQueryRetriever
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai.llms import GoogleGenerativeAI
from langchain_pinecone.vectorstores import PineconeVectorStore
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# User-friendly error messages
ERROR_MESSAGES = {
    "api_key_invalid": "Invalid API key. Please check your configuration.",
    "connection_error": "Unable to connect to the service. Please check your internet connection.",
    "retrieval_error": "Having trouble accessing the course materials. Please try again.",
    "processing_error": "Error processing your request. Please try rephrasing your question.",
    "initialization_error": "System initialization failed. Please contact support.",
    "general_error": "Something unexpected happened. Please try again.",
}


class RAGEngine:
    """RAG Engine for document retrieval and question answering"""
    
    def __init__(self):
        self.embeddings = None
        self.vector_stores = {}
        self.retrievers = {}
        self.llm = None
        self.model_name = "gemini-1.5-pro"  # Default model
        self.pinecone_client = None
        self.initialized = False
        
    def initialize(self, google_api_key: str, pinecone_api_key: str, model_name: str = "gemini-1.5-pro"):
        """Initialize the RAG engine with API keys"""
        try:
            logger.info("Initializing RAG engine...")
            
            # Set environment variables
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["PINECONE_API_KEY"] = pinecone_api_key
            
            self.model_name = model_name
            
            # Initialize embeddings
            logger.info("Initializing HuggingFace embeddings...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            
            # Initialize Pinecone
            logger.info("Initializing Pinecone connection...")
            self.pinecone_client = Pinecone(api_key=pinecone_api_key)
            
            # Initialize vector stores for different subjects
            self._initialize_vector_stores()
            
            # Initialize LLM
            logger.info(f"Initializing LLM with model: {model_name}")
            self.llm = GoogleGenerativeAI(model=model_name)
            
            # Initialize retrievers
            self._initialize_retrievers()
            
            self.initialized = True
            logger.info("RAG engine initialized successfully")
            return True, "RAG engine initialized successfully"
            
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {str(e)}")
            return False, f"Failed to initialize: {str(e)}"
    
    def _initialize_vector_stores(self):
        """Initialize Pinecone vector stores"""
        try:
            index_name = "semester-books"
            subjects = [
                "linear_algebra",
                "discrete_structures",
                "calculas_&_analytical_geometry",
            ]
            
            for subject in subjects:
                logger.info(f"Setting up vector store for subject: {subject}")
                self.vector_stores[subject] = PineconeVectorStore(
                    index_name=index_name,
                    embedding=self.embeddings,
                    namespace=subject
                )
            
            logger.info("All vector stores initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing vector stores: {str(e)}")
            raise
    
    def _initialize_retrievers(self):
        """Initialize retrievers for each subject"""
        try:
            subjects = {
                "linear_algebra": "lin",
                "discrete_structures": "dis",
                "calculas_&_analytical_geometry": "cal"
            }
            
            for subject, abbr in subjects.items():
                # MMR retriever
                self.retrievers[f"mmr_retriever_{abbr}"] = (
                    self.vector_stores[subject].as_retriever(
                        search_type="mmr",
                        search_kwargs={"k": 2, "lambda_mul": 0.7}
                    )
                )
                
                # MultiQuery retriever
                self.retrievers[f"multiquery_retriever_{abbr}"] = (
                    MultiQueryRetriever.from_llm(
                        retriever=self.vector_stores[subject].as_retriever(
                            search_type="similarity",
                            search_kwargs={"k": 2, "namespace": subject}
                        ),
                        llm=self.llm
                    )
                )
            
            self.retrievers["llm"] = self.llm
            logger.info("All retrievers initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing retrievers: {str(e)}")
            raise
    
    def format_docs(self, retrieved_docs):
        """Format retrieved documents for context"""
        try:
            return "\n\n".join(doc.page_content for doc in retrieved_docs)
        except Exception as e:
            logger.error(f"Error formatting documents: {str(e)}")
            return "Error retrieving document content"
    
    def answer_from_subject(self, query: str, subject: str) -> Dict[str, Any]:
        """
        Answer a query from a specific subject
        
        Args:
            query: The question to answer
            subject: One of ['linear_algebra', 'discrete_structures', 'calculus']
            
        Returns:
            Dict with answer, sources, and metadata
        """
        try:
            logger.info(f"Processing query for subject: {subject}")
            
            # Map subject to retriever abbreviation
            subject_map = {
                "linear_algebra": "lin",
                "discrete_structures": "dis",
                "calculus": "cal",
                "calculas_&_analytical_geometry": "cal"
            }
            
            abbr = subject_map.get(subject, "lin")
            retriever_key = f"multiquery_retriever_{abbr}"
            
            if retriever_key not in self.retrievers:
                raise ValueError(f"Invalid subject: {subject}")
            
            # Create the RAG chain
            parallel_chain = RunnableParallel({
                "context": self.retrievers[retriever_key] | RunnableLambda(self.format_docs),
                "question": RunnablePassthrough(),
            })
            
            prompt = PromptTemplate.from_template("""
                You are a helpful academic tutor helping a student with their coursework.
                You have access to relevant sections from their course textbook.

                Course Material Context:
                {context}

                Student's Question: {question}

                Instructions:
                - Answer the question using the provided course material context
                - Explain concepts step-by-step in simple terms
                - Include examples or analogies when helpful
                - If the question asks for "steps" or "method", provide a clear numbered list
                - If asking about general concepts, provide the standard method from the textbook
                - For sample problems, create appropriate examples if none are in the context
                - If the context is insufficient, provide what you can and mention what additional information might be helpful

                Provide a clear, educational response:
            """)
            
            parser = StrOutputParser()
            main_chain = parallel_chain | prompt | self.llm | parser
            
            # Execute the chain
            result = main_chain.invoke(query)
            
            logger.info("Query processed successfully")
            return {
                "answer": result,
                "subject": subject,
                "sources": [subject],
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                "answer": ERROR_MESSAGES["retrieval_error"],
                "subject": subject,
                "sources": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def answer_general_query(self, query: str) -> Dict[str, Any]:
        """
        Answer a general query by detecting the subject and routing appropriately
        
        Args:
            query: The question to answer
            
        Returns:
            Dict with answer, sources, and metadata
        """
        try:
            # Simple subject detection based on keywords
            query_lower = query.lower()
            
            if any(keyword in query_lower for keyword in ["matrix", "vector", "linear", "eigenvalue", "determinant"]):
                return self.answer_from_subject(query, "linear_algebra")
            elif any(keyword in query_lower for keyword in ["graph", "logic", "set", "combinatorics", "discrete", "proof"]):
                return self.answer_from_subject(query, "discrete_structures")
            elif any(keyword in query_lower for keyword in ["derivative", "integral", "limit", "calculus", "geometry"]):
                return self.answer_from_subject(query, "calculus")
            else:
                # Default to linear algebra if no clear subject detected
                return self.answer_from_subject(query, "linear_algebra")
                
        except Exception as e:
            logger.error(f"Error in general query: {str(e)}")
            return {
                "answer": ERROR_MESSAGES["processing_error"],
                "sources": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the RAG engine"""
        return {
            "initialized": self.initialized,
            "model": self.model_name,
            "subjects_available": list(self.vector_stores.keys()),
            "retrievers_count": len(self.retrievers)
        }


# Global RAG engine instance
rag_engine = RAGEngine()
