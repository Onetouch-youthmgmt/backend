from fastapi import APIRouter, Request, Depends
from auth.auth import verify_jwt_token
from services.sabha_center_service import get_all_sabha_centers, get_sabha_center_by_id, create_new_sabha_center, update_sabha_center_by_id, delete_sabha_center_by_id
from schemas.sabha_center_schema import SabhaCenterCreate, SabhaCenterResponse


router = APIRouter(
    prefix="/sabha_centers",
    tags=["sabha_centers"],
    dependencies=[Depends(verify_jwt_token)],
)


@router.get("/")
async def get_sabha_centers(request: Request)->list[SabhaCenterResponse]:
    """Get all sabha centers
    Args:
        request: FastAPI Request object
    Returns:
        List of SabhaCenterResponse objects
    """
    sabha_centers = get_all_sabha_centers()
    return [SabhaCenterResponse.model_validate(sabha_center) for sabha_center in sabha_centers]

@router.get("/{sabha_center_id}")
async def get_sabha_center(request: Request, sabha_center_id: int)->SabhaCenterResponse:
    """Get a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to retrieve
    Returns:
        SabhaCenterResponse object
    """
    sabha_center = get_sabha_center_by_id(sabha_center_id)
    return SabhaCenterResponse.model_validate(sabha_center)

@router.post("/")
async def create_sabha_center(request: Request, sabha_center: SabhaCenterCreate)->dict:
    """Create a new sabha center
    Args:
        request: FastAPI Request object
        sabha_center: SabhaCenterCreate object
    Returns:
        message that the sabha center is created successfully with the sabha center's city
    """
    return create_new_sabha_center(sabha_center)

@router.put("/{sabha_center_id}")
async def update_sabha_center(request: Request, sabha_center_id: int, sabha_center: SabhaCenterCreate)->dict:
    """Update a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to update
        sabha_center: SabhaCenterCreate object
    Returns:
        message that the sabha center is updated successfully with the sabha center's city
    """
    return update_sabha_center_by_id(sabha_center_id, sabha_center)

@router.delete("/{sabha_center_id}")
async def delete_sabha_center(request: Request, sabha_center_id: int)->dict:
    """Delete a sabha center by ID
    Args:
        request: FastAPI Request object
        sabha_center_id: ID of the sabha center to delete
    Returns:
        message that the sabha center is deleted successfully with the sabha center's city
    """
    return delete_sabha_center_by_id(sabha_center_id)
