import asyncio
import json
import random
import websockets

STUDENTS = [
    {"student_id": "ST101", "student_name": "أحمد علي", "room": "Room_A"},
    {"student_id": "ST102", "student_name": "عمر خالد", "room": "Room_B"},
    {"student_id": "ST103", "student_name": "سارة محمد", "room": "Room_A"},
    {"student_id": "ST104", "student_name": "محمد حسن", "room": "Room_C"},
]

STATUSES = ["Valid", "Valid", "Valid", "Expired"]

async def send_attendance_data():
    uri = "ws://localhost:8000/ws"
  
    async with websockets.connect(uri, origin=None) as websocket:
        print("تم الاتصال بالسيرفر، جاري إرسال القراءات...")
        while True:
            student = random.choice(STUDENTS)
            badge_status = random.choice(STATUSES)
            
            data = {
                "student_id": student["student_id"],
                "student_name": student["student_name"],
                "room": student["room"],
                "badge_status": badge_status
            }
            
            await websocket.send(json.dumps(data, ensure_ascii=False))
            print(f"تم إرسال: {data}")
            await asyncio.sleep(3)

if __name__ == "__main__":
    try:
        asyncio.run(send_attendance_data())
    except KeyboardInterrupt:
        print("\nتم إيقاف المحاكي.")