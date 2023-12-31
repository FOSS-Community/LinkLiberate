from pathlib import Path
from typing import List
from redis import Redis

from fastapi import (
    FastAPI,
    Form,
    Request,
    Response,
    HTTPException,
    status,
)
from fastapi.responses import (
    PlainTextResponse,
    HTMLResponse,
    RedirectResponse,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from typing import Annotated
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from .utils import generate_uuid, make_proper_url

limiter = Limiter(key_func=get_remote_address)
app: FastAPI = FastAPI(title="link-liberate")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins: List[str] = ["*"]

BASE_URL: str = r"127.0.0.1:8080"

BASE_DIR: Path = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates: Jinja2Templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

redis = Redis(host="localhost", port=6379)


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/liberate", response_class=HTMLResponse)
async def web(request: Request) -> Response:
    return templates.TemplateResponse("liberate.html", {"request": request})


@app.post("/liberate", response_class=PlainTextResponse)
@limiter.limit("100/minute")
async def web_post(
    request: Request, content: Annotated[str, Form()]
) -> PlainTextResponse:
    try:
        link: str = make_proper_url(content)
        uuid: str = generate_uuid()
        if redis.exists(uuid):
            uuid = generate_uuid()
        redis.set(uuid, link)
    except Exception as e:
        raise HTTPException(
            detail=f"There was an error uploading the file: {e}",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return PlainTextResponse(f"{BASE_URL}/{uuid}", status_code=status.HTTP_201_CREATED)


@app.get("/{uuid}", response_class=RedirectResponse)
async def get_link(request: Request, uuid: str) -> RedirectResponse:
    path: str = f"data/{uuid}"
    try:
        link: str = str(redis.get(uuid))[2:-1]
        return RedirectResponse(url=link, status_code=status.HTTP_301_MOVED_PERMANENTLY)
    except Exception as e:
        raise HTTPException(
            detail=f"404: The Requested Resource is not found: {e}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
