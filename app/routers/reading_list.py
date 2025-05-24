from fastapi import APIRouter

router = APIRouter(prefix="/reading-list", tags=["reading_list"])

@router.get("/")
def get_reading_list():
    return {"message": "Reading list will go here"}
