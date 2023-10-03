from fastapi import FastAPI
from routes.v1 import users
from Database.mongoDBConnection import database
from Configs import settings

app = FastAPI()

# Include API routes
app.include_router(users.router, prefix="/v1/users")


# Dependency Injection for MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    await database.client.start_session()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.client.close()
