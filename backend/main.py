from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import anthropic
import os
from dotenv import load_dotenv
from connection.manager import ConnectionManager

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            with client.messages.stream(
                max_tokens=1024,
                messages=[{"role": "user", "content": data}],
                model="claude-3-opus-20240229",
            ) as stream:
                for chunk in stream:
                    if chunk.type == "content_block_delta":
                        await manager.send_personal_message(
                            chunk.delta.text, websocket
                        )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
