from pathlib import Path
from typing import List

from fastapi import FastAPI, Form, Request, Response, HTTPException, status, Depends
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
from sqlalchemy.orm import Session

from .utils import generate_uuid, make_proper_url
from .models import Base, LiberatedLink
from .database import engine, get_db

limiter = Limiter(key_func=get_remote_address)
app: FastAPI = FastAPI(title="link-liberate")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
Base.metadata.create_all(bind=engine)
origins: List[str] = ["*"]

BASE_URL: str = r"http://0.0.0.0:8080"

BASE_DIR: Path = Path(__file__).resolve().parent

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates: Jinja2Templates = Jinja2Templates(directory=str(Path(BASE_DIR, "templates")))


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/liberate", response_class=HTMLResponse)
async def web(request: Request) -> Response:
    return templates.TemplateResponse("liberate.html", {"request": request})


@app.post("/liberate", response_class=HTMLResponse)
@limiter.limit("100/minute")
async def web_post(
    request: Request, content: Annotated[str, Form()], customString: Annotated[str, Form()] = None, db: Session = Depends(get_db)
) -> PlainTextResponse:
    try:
        link: str = make_proper_url(content)
        uuid: str = customString
        if uuid is None:
            uuid: str = generate_uuid()
            if db.query(LiberatedLink).filter(LiberatedLink.uuid == uuid).first():
                uuid = generate_uuid()
        new_liberated_link = LiberatedLink(uuid=uuid, link=link)
        db.add(new_liberated_link)
        db.commit()
        db.refresh(new_liberated_link)
        context = {"link": link, "short": f"{BASE_URL}/{uuid}"}
    except Exception as e:
        raise HTTPException(
            detail=f"There was an error uploading the file: {e}",
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return templates.TemplateResponse(
        request=request, name="showlibrate.html", context=context
    )


@app.get("/{uuid}", response_class=RedirectResponse)
async def get_link(
    request: Request, uuid: str, db: Session = Depends(get_db)
) -> RedirectResponse:
    path: str = f"data/{uuid}"
    try:
        link = db.query(LiberatedLink).filter(LiberatedLink.uuid == uuid).first()
        return RedirectResponse(
            url=link.link, status_code=status.HTTP_301_MOVED_PERMANENTLY
        )
    except Exception as e:
        raise HTTPException(
            detail=f"404: The Requested Resource is not found: {e}",
            status_code=status.HTTP_404_NOT_FOUND,
        )
