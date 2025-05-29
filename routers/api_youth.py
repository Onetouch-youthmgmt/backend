from sqlalchemy import UUID
from services.utility import sqlalchemy_to_pydantic_dict
from services.youth_service import create_new_youth, deactivate_youth, get_all_youths, get_youth_by_id, update_youth_by_id
from schemas.youth_schema import YouthCreate, YouthResponse
from models.youth import Youth
from models.karyakarta import Karyakarta
from auth.auth_decorators import authorize
from enums.user import UserRole
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session 
from database.database import get_db

router = APIRouter(
    prefix="/youths",
    tags=["youths"],
)

@router.get("/")
@authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def get_youths(request: Request, db: Session = Depends(get_db))->list[YouthResponse]: 
    """Get all youths 
    Args:
        request: FastAPI Request object
        db: Database session
    Returns:
        List of YouthResponse objects
    Raises:
        HTTPException: If sabha_center_id is not provided
    """
    sabha_center_id = request.query_params.get("sabha_center_id")
    if not sabha_center_id:
        raise HTTPException(
            status_code=400,
            detail="sabha_center_id query parameter is required"
        )
    
    youths = get_all_youths(sabha_center_id, db)
    print(youths)
    youths_pydanticmodel = [sqlalchemy_to_pydantic_dict(youth) for youth in youths]
    return [YouthResponse.model_validate(youth) for youth in youths_pydanticmodel]

@router.get("/{youth_id}")
@authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def get_youth(request: Request, youth_id: int, db: Session = Depends(get_db))->YouthResponse:
    """Get a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to retrieve
        db: Database session
    Returns:
        YouthResponse object
    """
    youth = get_youth_by_id(youth_id, db)
    print(youth)
    youth_pydanticmodel = sqlalchemy_to_pydantic_dict(youth)
    return YouthResponse.model_validate(youth_pydanticmodel)

@router.delete('/{youth_id}')
@authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def deactivate_youth_by_id(request: Request, youth_id: int, db: Session = Depends(get_db))->dict:
    """Deactivate a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to deactivate
        db: Database session
    Returns:    
        message that the youth is deactivated successfully with the youth's first and last name
    """
    return deactivate_youth(youth_id, db)

@router.post('/')
@authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def create_youth(request: Request, youth: YouthCreate, db: Session = Depends(get_db))->dict:
    """Create a new youth
    Args:
        request: FastAPI Request object
        youth: YouthCreate object
        db: Database session
    Returns:
        message that the youth is created successfully with the youth's first and last name 
    """
    return create_new_youth(youth, db)
    
@router.put('/{youth_id}')
@authorize([UserRole.ADMIN, UserRole.KARYAKARTA])
async def update_youth(request: Request, youth_id: int, youth: YouthCreate, db: Session = Depends(get_db))->dict:
    """Update a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to update
        youth: YouthCreate object
        db: Database session
    Returns:
        message that the youth is updated successfully with the youth's first and last name
    """
    return update_youth_by_id(youth_id, youth, db)
