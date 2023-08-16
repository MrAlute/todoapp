from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_company_name():
    return {"developer_name": "Abi Chioduye, Full Stack Developer"}


@router.get("/employees")
async def number_of_employees():
    return 162


