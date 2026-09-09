from fastapi import APIRouter, HTTPException, Request, Depends
from auth.auth import verify_jwt_token
from services.sabha_service import create_new_sabha, delete_sabha_by_id, get_all_sabhas, get_sabha_by_id, update_sabha_by_id
from schemas.sabha_schema import SabhaCreate, SabhaResponse

router = APIRouter(
    prefix="/sabhas",
    tags=["sabhas"],
     dependencies=[Depends(verify_jwt_token)],
)

@router.get("/")
async def get_sabhas(request: Request)->list[SabhaResponse]:
    """Get all sabhas
    Args:
        request: FastAPI Request object
    Returns:
        List of SabhaResponse objects
    Query Parameters:
        sabha_center_id: ID of the sabha center to filter sabhas
    """
    sabha_center_id = request.query_params.get("sabha_center_id")
    if not sabha_center_id:
        raise HTTPException(status_code=400, detail="sabha_center_id is required")
    sabhas = get_all_sabhas(sabha_center_id)
    return [SabhaResponse.model_validate(sabha) for sabha in sabhas]

@router.get("/{sabha_id}")
async def get_sabha(request: Request, sabha_id: int)->SabhaResponse:
    """Get a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to retrieve
    Returns:
        SabhaResponse object
    """
    sabha = get_sabha_by_id(sabha_id)
    return SabhaResponse.model_validate(sabha)

@router.post("/")
async def create_sabha(request: Request, sabha: SabhaCreate)->dict:
    """Create a new sabha
    Args:
        request: FastAPI Request object
        sabha: SabhaCreate object
    Returns:
        dict
    """
    return create_new_sabha(sabha)

@router.put("/{sabha_id}")
async def update_sabha(request: Request, sabha_id: int, sabha: SabhaCreate)->dict:
    """Update a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to update
        sabha: SabhaCreate object
    Returns:
        dict
    """
    return update_sabha_by_id(sabha_id, sabha)

@router.delete("/{sabha_id}")
async def delete_sabha(request: Request, sabha_id: int)->dict:
    """Delete a sabha by ID
    Args:
        request: FastAPI Request object
        sabha_id: ID of the sabha to delete
    Returns:
        dict
    """
    return delete_sabha_by_id(sabha_id)
