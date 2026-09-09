from auth.auth import verify_jwt_token
from services.youth_service import create_new_youth, delete_youth_by_id, get_all_youths, get_youth_by_id, get_youths_by_karyakarta_id, update_youth_by_id
from schemas.youth_schema import YouthCreate, YouthKaryakartaResponse, YouthResponse
from fastapi import APIRouter, HTTPException, Request, Depends

router = APIRouter(
    prefix="/youths",
    tags=["youths"],
     dependencies=[Depends(verify_jwt_token)],
)

@router.get("/")
async def get_youths(request: Request)->list[YouthResponse]:
    """Get all youths
    Args:
        request: FastAPI Request object
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

    youths = get_all_youths(sabha_center_id)
    return [YouthResponse.model_validate(youth) for youth in youths]

@router.get("/get-all-karyakarta")
async def get_all_karyakarta(request: Request)->list[YouthResponse]:

    """Get all youths who are karyakartas

    Args:
        request: FastAPI Request object

    Returns:
        List of YouthResponse objects for youths who are also karyakartas

    Raises:
        HTTPException: If sabha_center_id is not provided
    """
    sabha_center_id = request.query_params.get("sabha_center_id")
    if not sabha_center_id:
        raise HTTPException(
            status_code=400,
            detail="sabha_center_id query parameter is required"
        )
    youths = get_all_youths(sabha_center_id)
    karyakarta_youths = [youth for youth in youths if youth.get('is_karyakarta', False)]

    return [YouthResponse.model_validate(karyakarta) for karyakarta in karyakarta_youths]

@router.get("/{youth_id}")
async def get_youth(request: Request, youth_id: int)->YouthResponse:
    """Get a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to retrieve
    Returns:
        YouthResponse object
    """
    youth = get_youth_by_id(youth_id)
    return YouthResponse.model_validate(youth)

@router.get("/by-karyakarta/{karyakarta_id}")
async def get_youths_by_karyakarta(request: Request, karyakarta_id: int)->list[YouthKaryakartaResponse]:
    """Get all youths managed by a specific karyakarta
    Args:
        request: FastAPI Request object
        karyakarta_id: ID of the karyakarta
    Returns:
        List of YouthResponse objects for youths managed by the karyakarta
    """
    karyakarta_followedup_youths = get_youths_by_karyakarta_id(karyakarta_id)
    return [YouthKaryakartaResponse.model_validate(youth) for youth in karyakarta_followedup_youths]

@router.delete('/{youth_id}')
async def delete_youth(request: Request, youth_id: int)->dict:
    """Deactivate a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to deactivate
    Returns:
        message that the youth is deactivated successfully with the youth's first and last name
    """
    return delete_youth_by_id(youth_id)

@router.post('/')
async def create_youth(request: Request, youth: YouthCreate)->dict:
    """Create a new youth
    Args:
        request: FastAPI Request object
        youth: YouthCreate object
    Returns:
        message that the youth is created successfully with the youth's first and last name
    """
    return create_new_youth(youth)

@router.put('/{youth_id}')
async def update_youth(request: Request, youth_id: int, youth: YouthCreate)->dict:
    """Update a youth by ID
    Args:
        request: FastAPI Request object
        youth_id: ID of the youth to update
        youth: YouthCreate object
    Returns:
        message that the youth is updated successfully with the youth's first and last name
    """
    return update_youth_by_id(youth_id, youth)
