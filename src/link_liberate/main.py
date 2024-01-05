from pathlib import Path
from typing import List

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

from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

from .utils import generate_uuid

limiter = Limiter(key_func=get_remote_address)
app: FastAPI = FastAPI(title="link-liberate")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

origins: List[str] = ["*"]

BASE_URL: str = r"127.0.0.1:8000"

BASE_DIR: Path = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates: Jinja2Templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))

large_uuid_storage: List[str] = []


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/liberate", response_class=HTMLResponse)
async def web(request: Request) -> Response:
    return templates.TemplateResponse("web.html", {"request": request})


@app.post("/liberate", response_class=PlainTextResponse)
@limiter.limit("100/minute")
async def web_post(request: Request, content: str = Form(...)) -> PlainTextResponse:
    try:
        link: bytes = content.encode()
        uuid: str = generate_uuid()
        if uuid in large_uuid_storage:
            uuid = generate_uuid()
        path: str = f"data/{uuid}"
        with open(path, "wb") as f:
            f.write(link)
            large_uuid_storage.append(uuid)
    except Exception:
        raise HTTPException(
            detail="There was an error uploading the file",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    return PlainTextResponse(f"{BASE_URL}/{uuid}", status_code=status.HTTP_201_CREATED)


@app.post("/")
@limiter.limit("100/minute")
async def post_as_a_file(
    request: Request, content: str = Form(...)
) -> PlainTextResponse:
    try:
        uuid: str = generate_uuid()
        if uuid in large_uuid_storage:
            uuid = generate_uuid()
        path: str = f"data/{uuid}"
        val: str = "/".join(path.split("/")[1:])
        with open(path, "wb") as f:
            f.write(content.encode())
            large_uuid_storage.append(uuid)
    except Exception:
        raise HTTPException(
            detail="There was an error uploading the file",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return PlainTextResponse(val, status_code=status.HTTP_201_CREATED)


@app.get("/{uuid}")
async def get_link(uuid: str) -> RedirectResponse:
    path: str = f"data/{uuid}"
    try:
        with open(path, "wb") as f:
            original_link: str = f.read().decode("utf-8")
            return RedirectResponse(original_link)
    except Exception:
        raise HTTPException(
            detail="404: The Requested Resource is not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
