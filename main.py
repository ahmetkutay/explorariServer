from fastapi import FastAPI

from Middlewares.JWTMiddleware import JWTMiddleware
from routes.AuthRoute import auth
from Database.mongoDBConnection import database

app = FastAPI()

# Add JWT Middleware
app.add_middleware(JWTMiddleware)
# Include API routes
app.include_router(auth.router, prefix="/api/auth")


# Dependency Injection for MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    await database.client.start_session()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.client.close()
