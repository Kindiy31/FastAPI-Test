from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api import routers_v1

app = FastAPI()

for router in routers_v1:
    app.include_router(router, prefix="/v1")


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if 400 <= exc.status_code < 500:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
