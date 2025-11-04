"""
RAG Routes for FastAPI
Handles RAG-based chat queries and document management
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from typing import Optional, List
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import asyncio

from database.db import get_db
from routes.loginPage import get_current_user
from rag_engine import rag_engine
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class RAGChatRequest(BaseModel):
    question: str
    context: Optional[str] = "general"
    language: Optional[str] = "en-US"
    subject: Optional[str] = None  # specific subject or None for auto-detection


class RAGInitRequest(BaseModel):
    google_api_key: str
    pinecone_api_key: str
    model_name: Optional[str] = "gemini-1.5-pro"


@router.post("/rag/initialize")
async def initialize_rag(
    request: RAGInitRequest,
    current_user: dict = Depends(get_current_user),
    db: psycopg2.extensions.connection = Depends(get_db)
):
    """
    Initialize the RAG engine with API keys
    This should be called once on startup or when keys are updated
    """
    try:
        # Only admin can initialize the RAG engine
        if current_user.get("role", "").lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can initialize the RAG engine"
            )
        
        success, message = rag_engine.initialize(
            google_api_key=request.google_api_key,
            pinecone_api_key=request.pinecone_api_key,
            model_name=request.model_name
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=message
            )
        
        # Log the initialization activity
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO activities (type, user_id, action, target)
            VALUES (%s, %s, %s, %s)
        """, ("rag_init", current_user["id"], "initialized", "RAG Engine"))
        db.commit()
        
        return {
            "success": True,
            "message": message,
            "status": rag_engine.get_status()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initializing RAG engine: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/rag/chat")
async def rag_chat(
    request: RAGChatRequest,
    current_user: dict = Depends(get_current_user),
    db: psycopg2.extensions.connection = Depends(get_db)
):
    """
    Process a RAG-based chat query
    Supports auto-detection of subject or explicit subject specification
    """
    try:
        # Check if RAG engine is initialized
        if not rag_engine.initialized:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="RAG engine is not initialized. Please contact administrator."
            )
        
        # Process the query
        if request.subject:
            # Query specific subject
            result = rag_engine.answer_from_subject(request.question, request.subject)
        else:
            # Auto-detect subject and answer
            result = rag_engine.answer_general_query(request.question)
        
        # Log the chat activity
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO activities (type, user_id, action, target)
            VALUES (%s, %s, %s, %s)
        """, ("rag_chat", current_user["id"], "asked", request.question[:100]))
        db.commit()
        
        return {
            "answer": result.get("answer", ""),
            "sources": result.get("sources", []),
            "subject": result.get("subject", "unknown"),
            "timestamp": result.get("timestamp"),
            "type": "rag"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing RAG query: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/rag/upload")
async def upload_documents(
    files: List[UploadFile] = File(...),
    category: Optional[str] = Form("general"),
    current_user: dict = Depends(get_current_user),
    db: psycopg2.extensions.connection = Depends(get_db)
):
    """
    Upload documents to the knowledge base
    This is a placeholder for future document ingestion functionality
    """
    try:
        # Only admin can upload documents
        if current_user.get("role", "").lower() != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only administrators can upload documents"
            )
        
        uploaded_files = []
        for file in files:
            # Validate file type
            allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
            if file.content_type not in allowed_types:
                continue
            
            # TODO: Implement document processing and Pinecone upload
            # For now, just log the upload
            uploaded_files.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size
            })
        
        # Log the upload activity
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO activities (type, user_id, action, target)
            VALUES (%s, %s, %s, %s)
        """, ("document_upload", current_user["id"], "uploaded", f"{len(uploaded_files)} documents"))
        db.commit()
        
        return {
            "success": True,
            "uploaded_count": len(uploaded_files),
            "files": uploaded_files,
            "message": "Documents uploaded successfully. Processing will begin shortly."
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading documents: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rag/status")
async def get_rag_status(current_user: dict = Depends(get_current_user)):
    """Get the current status of the RAG engine"""
    try:
        status = rag_engine.get_status()
        return status
    except Exception as e:
        logger.error(f"Error getting RAG status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/rag/subjects")
async def get_available_subjects(current_user: dict = Depends(get_current_user)):
    """Get list of available subjects in the knowledge base"""
    try:
        if not rag_engine.initialized:
            return {"subjects": [], "initialized": False}
        
        subjects = [
            {"id": "linear_algebra", "name": "Linear Algebra", "description": "Matrix operations, vectors, eigenvalues"},
            {"id": "discrete_structures", "name": "Discrete Structures", "description": "Logic, graphs, combinatorics"},
            {"id": "calculus", "name": "Calculus & Analytical Geometry", "description": "Derivatives, integrals, limits"}
        ]
        
        return {
            "subjects": subjects,
            "initialized": True
        }
    except Exception as e:
        logger.error(f"Error getting subjects: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/chat")
async def legacy_chat(
    question: str = Form(...),
    context: Optional[str] = Form("general"),
    language: Optional[str] = Form("en-US"),
    documents: Optional[List[UploadFile]] = File(None),
    current_user: dict = Depends(get_current_user),
    db: psycopg2.extensions.connection = Depends(get_db)
):
    """
    Legacy chat endpoint for backwards compatibility
    Routes requests to either RAG or simple chat based on context
    """
    try:
        # Log the chat activity
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO activities (type, user_id, action, target)
            VALUES (%s, %s, %s, %s)
        """, ("chat", current_user["id"], "asked", question[:100]))
        db.commit()
        
        # If context is documents or if documents are uploaded, use RAG
        if context == "documents" or documents:
            if rag_engine.initialized:
                request = RAGChatRequest(
                    question=question,
                    context=context,
                    language=language
                )
                result = rag_engine.answer_general_query(question)
                return {
                    "answer": result.get("answer", ""),
                    "response": result.get("answer", ""),  # For backwards compatibility
                    "sources": result.get("sources", []),
                    "type": "rag"
                }
            else:
                return {
                    "answer": "RAG system is not initialized. Please contact administrator.",
                    "response": "RAG system is not initialized. Please contact administrator.",
                    "type": "error"
                }
        
        # Otherwise, return a simple response
        return {
            "answer": f"I received your question: '{question}'. The RAG system will be integrated here for document-based queries.",
            "response": f"I received your question: '{question}'. The RAG system will be integrated here for document-based queries.",
            "type": "general"
        }
    
    except Exception as e:
        logger.error(f"Error in legacy chat: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
