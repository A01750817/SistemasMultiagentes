import fastapi
from fastapi import WebSocket, WebSocketDisconnect
import uvicorn

app = fastapi.FastAPI()
ws_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    ws_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_connections.remove(websocket)
        print("Cliente desconectado")

async def send_message(message: str):
    for connection in ws_connections:
        await connection.send_text(message)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
