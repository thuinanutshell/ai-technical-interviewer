import uuid
import tempfile
from typing import Optional, List
from pathlib import Path
import traceback

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlmodel import Session, select

import pymupdf4llm

from app.models.resume import Resume, ResumeCreate, ResumePublic
from app.models.user import User
from app.api.deps import get_current_user, SessionDep

router = APIRouter(prefix="/resumes", tags=["Resumes"])

ALLOWED_EXTENSIONS = {".pdf"}


def parse_resume_to_markdown(file_bytes: bytes) -> str:
    """Write PDF to a temp file and extract markdown using pymupdf4llm."""
    try:
        with tempfile.NamedTemporaryFile(delete=True, suffix=".pdf") as tmp:
            tmp.write(file_bytes)
            tmp.flush()

            markdown = pymupdf4llm.to_markdown(tmp.name)
            if not markdown or not markdown.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Could not extract text from PDF. The file may be corrupted or contain only images.",
                )

        return markdown.strip()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse PDF: {str(e)}",
        )


@router.post("/", response_model=ResumePublic, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: Session = SessionDep,
):
    """Upload a resume PDF and store its parsed markdown content."""
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    try:
        file_bytes = await file.read()
        parsed_data = parse_resume_to_markdown(file_bytes)

        resume = Resume(
            parsed_data=parsed_data,
            pdf_url=None,
            user_id=current_user.id,
        )

        session.add(resume)
        session.commit()
        session.refresh(resume)
        return resume

    except HTTPException:
        raise
    except Exception as e:
        print("UPLOAD RESUME ERROR:", traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )
