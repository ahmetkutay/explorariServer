from fastapi import FastAPI
from routes.UserRoute import users
from Database.mongoDBConnection import database

app = FastAPI()

# Include API routes
app.include_router(users.router, prefix="/api/users")


# Dependency Injection for MongoDB connection
@app.on_event("startup")
async def startup_db_client():
    await database.client.start_session()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.client.close()
