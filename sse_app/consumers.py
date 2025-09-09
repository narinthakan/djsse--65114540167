# sse_app/consumers.py
from django.http import HttpResponse
import time
import random
import json

def event_stream():
    """จำลองการส่งข้อมูลตำแหน่งเครื่องบินและสถานะ"""
    # จุดเริ่มต้น (อนุสาวรีย์ชัยฯ) และปลายทาง (สนามหลวง)
    start_lat, start_lng = 13.7649, 100.5383  # กรุงเทพ (อนุสาวรีย์ชัยฯ)
    end_lat, end_lng = 15.2467, 104.8570      # อุบลราชธานี (สนามบินอุบลฯ)
    steps = 100
    direction = 1  # 1 = ไปสนามหลวง, -1 = กลับกรุงเทพ
    step = 0
    while True:
        t = step / steps
        if direction == 1:
            lat = start_lat + (end_lat - start_lat) * t
            lng = start_lng + (end_lng - start_lng) * t
        else:
            lat = end_lat + (start_lat - end_lat) * t
            lng = end_lng + (start_lng - end_lng) * t
        if step < 10:
            status = "Takeoff"
        elif step < steps - 10:
            status = "In Flight"
        elif step < steps:
            status = "Landing"
        else:
            status = "Landed"
        data = {
            "latitude": lat,
            "longitude": lng,
            "status": status
        }
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(0.1)
        step += 1
        if step > steps:
            step = 0
            direction *= -1

def sse_view(request):
    """View สำหรับส่งข้อมูลผ่าน SSE"""
    return HttpResponse(event_stream(), content_type='text/event-stream')