from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from auth.auth import verify_jwt_token
from enums.user import UserRole
from services.utility import sqlalchemy_to_pydantic_dict
from services.sabha_service import create_new_sabha, delete_sabha_by_id, get_all_sabhas, get_sabha_by_id, update_sabha_by_id
from database.database import get_db
from models.sabha import Sabha
from schemas.sabha_schema import SabhaCreate, SabhaResponse

router = APIRouter(
    prefix="/sabhas",
    tags=["sabhas"],
     dependencies=[Depends(verify_jwt_token)],
)

@router.get("/")
async def get_sabhas(request: Request, db: Session = Depends(get_db))->list[SabhaResponse]:
    """Get all sabhas
    Args:
        request: FastAPI Request object
        db: Database session
    Returns:
        List of SabhaResponse objects
    Query Parameters:
        sabha_center_id: ID of the sabha center to filter sabhas
    """
    sabha_center_id = request.query_params.get("sabha_center_id")
    if not sabha_center_id:
        raise HTTPException(status_code=400, detail="sabha_center_id is required")
    sabhas = get_all_sabhas(sabha_center_id, db)
    sabhas_pydanticmodel = [sqlalchemy_to_pydantic_dict(sabha) for sabha in sabhas]
    return [SabhaResponse.model_validate(sabha) for sabha in sabhas_pydanticmodel]

@router.get("/{sabha_id}")
async def get_sabha(request: Request, sabha_id: int, db: Session = Depends(get_db))->SabhaResponse:
    """Get a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to retrieve
        db: Database session
    Returns:
        SabhaResponse object
    """
    sabha = get_sabha_by_id(sabha_id, db)
    sabha_pydanticmodel = sqlalchemy_to_pydantic_dict(sabha)
    return SabhaResponse.model_validate(sabha_pydanticmodel)

@router.post("/")
async def create_sabha(request: Request, sabha: SabhaCreate, db: Session = Depends(get_db))->dict:
    """Create a new sabha
    Args:
        request: FastAPI Request object
        sabha: SabhaCreate object
        db: Database session
    Returns:
        dict
    """
    return create_new_sabha(sabha, db)

@router.put("/{sabha_id}")
async def update_sabha(request: Request, sabha_id: int, sabha: SabhaCreate, db: Session = Depends(get_db))->dict:
    """Update a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to update
        sabha: SabhaCreate object
        db: Database session
    Returns:
        dict            
    """
    return update_sabha_by_id(sabha_id, sabha, db)

@router.delete("/{sabha_id}")
async def delete_sabha(request: Request, sabha_id: int, db: Session = Depends(get_db))->dict:
    """Delete a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to delete
        db: Database session
    Returns:
        dict    
    """
    return delete_sabha_by_id(sabha_id, db)
