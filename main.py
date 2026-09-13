from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List
import json
from database import SessionLocal, CheckIn, AttendanceAlert

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def get_index():
    return FileResponse("index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    db = SessionLocal()
    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            
          
            new_checkin = CheckIn(
                student_id=payload.get("student_id"),
                student_name=payload.get("student_name", "طالب")
            )
            db.add(new_checkin)
            
            # تحقق من التنبيهات
            if payload.get("badge_status") == "Expired":
                alert = AttendanceAlert(
                    student_id=payload.get("student_id"),
                    message="محاولة استخدام بطاقة منتهية الصلاحية",
                    alert_type="تنبيه أمني"
                )
                db.add(alert)
            
            db.commit()

           
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"Error: {e}")
        manager.disconnect(websocket)
    finally:
        db.close()