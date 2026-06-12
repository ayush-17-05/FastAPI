from fastapi import FastAPI
from app.routes.issues import router as issues_router
from todo_app.routes.todos import router as todos_router
from app.middlewares.timer import timing_middleware
from fastapi.middleware.cors import CORSMiddleware
from todo_app.routes.users import router as users_router

app = FastAPI()

# app.middleware("http")(timing_middleware)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(issues_router)

app.include_router(todos_router)
app.include_router(users_router)

