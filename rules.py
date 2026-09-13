from datetime import datetime, timedelta
from database import AttendanceAlert, CheckIn
from sqlalchemy.orm import Session


def analyze_checkin(
    db: Session,
    student_id: str,
    room: str,
    current_time: datetime,
    badge_status: str,
):
  alerts = []


  if badge_status != "Valid":
    alerts.append({
        "type": "INVALID_BADGE",
        "score": 90.0,
        "details": f"تم التبصيم ببطاقة حالتها: {badge_status}",
    })


  two_minutes_ago = current_time - timedelta(minutes=2)
  last_checkin = (
      db.query(CheckIn)
      .filter(
          CheckIn.student_id == student_id,
          CheckIn.timestamp >= two_minutes_ago,
      )
      .order_by(CheckIn.timestamp.desc())
      .first()
  )

  if last_checkin and last_checkin.room != room:
    alerts.append({
        "type": "DUPLICATE_ROOM_CHECKIN",
        "score": 100.0,
        "details": (
            f"سجل الطالب في قاعة {last_checkin.room} وقاعة {room} خلال أقل من"
            " دقيقتين"
        ),
    })

 
  for alert in alerts:
    db_alert = AttendanceAlert(
        student_id=student_id,
        alert_type=alert["type"],
        risk_score=alert["score"],
        details=alert["details"],
        timestamp=current_time,
    )
    db.add(db_alert)

  db.commit()
  return alerts