
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from auth.auth import verify_jwt_token
from services.utility import sqlalchemy_to_pydantic_dict
from services.sabha_center_service import get_all_sabha_centers, get_sabha_center_by_id, create_new_sabha_center, update_sabha_center_by_id, delete_sabha_center_by_id
from database.database import get_db
from enums.user import UserRole
from schemas.sabha_center_schema import SabhaCenterCreate, SabhaCenterResponse


router = APIRouter(
    prefix="/sabha_centers",
    tags=["sabha_centers"],
    dependencies=[Depends(verify_jwt_token)],  
)


@router.get("/")
async def get_sabha_centers(request: Request, db: Session = Depends(get_db))->list[SabhaCenterResponse]:
    """Get all sabha centers
    Args:
        request: FastAPI Request object
        db: Database session
    Returns:
        List of SabhaCenterResponse objects
    """
    sabha_centers = get_all_sabha_centers(db)
    sabha_centers_pydanticmodel = [sqlalchemy_to_pydantic_dict(sabha_center) for sabha_center in sabha_centers]
    return [SabhaCenterResponse.model_validate(sabha_center) for sabha_center in sabha_centers_pydanticmodel]

@router.get("/{sabha_center_id}")
async def get_sabha_center(request: Request, sabha_center_id: int, db: Session = Depends(get_db))->SabhaCenterResponse:
    """Get a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to retrieve
        db: Database session
    Returns:
        SabhaCenterResponse object
    """
    sabha_center = get_sabha_center_by_id(sabha_center_id, db)
    sabha_center_pydanticmodel = sqlalchemy_to_pydantic_dict(sabha_center)
    return SabhaCenterResponse.model_validate(sabha_center_pydanticmodel)

@router.post("/")
async def create_sabha_center(request: Request, sabha_center: SabhaCenterCreate, db: Session = Depends(get_db))->dict:
    """Create a new sabha center
    Args:
        request: FastAPI Request object
        sabha_center: SabhaCenterCreate object
        db: Database session
    Returns:
        message that the sabha center is created successfully with the sabha center's city
    """
    return create_new_sabha_center(sabha_center, db)

@router.put("/{sabha_center_id}")
async def update_sabha_center(request: Request, sabha_center_id: int, sabha_center: SabhaCenterCreate, db: Session = Depends(get_db))->dict:
    """Update a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to update
        sabha_center: SabhaCenterCreate object
        db: Database session
    Returns:
        message that the sabha center is updated successfully with the sabha center's city
    """     
    return update_sabha_center_by_id(sabha_center_id, sabha_center, db)

@router.delete("/{sabha_center_id}")
async def delete_sabha_center(request: Request, sabha_center_id: int, db: Session = Depends(get_db))->dict:
    """Delete a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to delete
        db: Database session
    Returns:
        message that the sabha center is deleted successfully with the sabha center's city
    """
    return delete_sabha_center_by_id(sabha_center_id, db)       