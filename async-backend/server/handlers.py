from fastapi import FastAPI



def on_startup(app: FastAPI):
    async def setup():
        from server.api import router
        app.include_router(router, prefix="/ai")
        # if DEBUG:
        from server.api_debug import router as debug_router
        app.include_router(debug_router, prefix="/ai/debug")

    return setup
