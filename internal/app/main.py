from fastapi import FastAPI
from pydantic import ValidationError
from internal.endpoints.routers import routers
from internal.schema.Response import WalletResponse,BaseNotEnoughFundsResponse
import uvicorn
#add CORS
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(routers)

@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    return WalletResponse(status=BaseNotEnoughFundsResponse.status, content="Bad request,422 non supported entity")


#if __name__ == "__main__":
    #uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


