import fastapi

router = fastapi.APIRouter()


@router.get('/healthz')
def health_check():
    return 'OK'