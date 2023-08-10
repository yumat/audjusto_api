from fastapi import FastAPI
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, group, members, pay, payback, schedule, attendance, task, done

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(group.router)
app.include_router(members.router)
app.include_router(pay.router)
app.include_router(payback.router)
app.include_router(schedule.router)
app.include_router(attendance.router)
# app.include_router(task.router)
# app.include_router(done.router)

handler = Mangum(app)