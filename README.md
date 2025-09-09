
# Server-Sent Events (SSE) คืออะไร?

Server-Sent Events (SSE) คือเทคโนโลยีสำหรับการส่งข้อมูลแบบเรียลไทม์จากฝั่งเซิร์ฟเวอร์ไปยังฝั่งไคลเอนต์ผ่าน HTTP โดยไม่ต้องให้ไคลเอนต์รีเฟรชหรือร้องขอข้อมูลใหม่ตลอดเวลา เหมาะสำหรับงานที่ต้องการอัปเดตข้อมูลสด เช่น แชท, แจ้งเตือน, ติดตามตำแหน่ง, แสดงข้อมูลเซ็นเซอร์ ฯลฯ

- SSE ใช้ HTTP connection เดียว (แบบ long-lived connection)
- ข้อมูลจะถูกส่งจาก server ไป client ฝั่งเดียว (one-way)
- รองรับในเบราว์เซอร์สมัยใหม่ผ่าน JavaScript (EventSource)

---

## วิธีใช้งาน SSE ใน Django

### 1. สร้าง View สำหรับ SSE

ตัวอย่างใน `sse_app/consumers.py`:
```python
def event_stream():
	while True:
		data = {"message": "Hello from server!"}
		yield f"data: {json.dumps(data)}\n\n"
		time.sleep(1)

def sse_view(request):
	return HttpResponse(event_stream(), content_type='text/event-stream')
```
- ฟังก์ชัน `event_stream` จะ yield ข้อมูลใหม่เรื่อย ๆ
- Content-Type ต้องเป็น `text/event-stream`

### 2. เพิ่ม URL สำหรับ SSE

ใน `sse_app/urls.py`:
```python
from . import consumers
urlpatterns = [
	path('sse/', consumers.sse_view, name='sse'),
]
```

### 3. ฝั่ง Frontend (HTML/JS)

```html
<script>
const eventSource = new EventSource('/sse/');
eventSource.onmessage = function(event) {
	const data = JSON.parse(event.data);
	// นำข้อมูลไปแสดงผล
	console.log(data);
};
</script>
```
- ใช้ `EventSource` เพื่อเชื่อมต่อกับ endpoint `/sse/`
- เมื่อ server ส่งข้อมูลใหม่ จะถูกเรียกใน onmessage

---

## หมายเหตุ
- SSE เหมาะกับการ push ข้อมูลจาก server ไป client แบบเรียลไทม์ (one-way)
- ถ้าต้องการสื่อสารสองทาง (bi-directional) ให้ใช้ WebSocket
- หาก deploy จริงควรใช้ server ที่รองรับ long-lived connection เช่น gunicorn + gevent หรือ daphne

---

## ตัวอย่างโปรเจกต์นี้
- ใช้ SSE ส่งตำแหน่งเครื่องบินแบบเรียลไทม์จาก Django backend ไปยังหน้าเว็บ (Leaflet map)
- ดูโค้ดตัวอย่างใน `sse_app/consumers.py` และ `sse_app/templates/sse_app/index.html`

## ขั้นตอนสำหรับรันโปรเจกต์ SSE
git clone https://github.com/narinthakan/djsse--65114540167.git
cd djsse

ติดตั้ง
pip install -r requirements.txt
pip install django-eventstream
python manage.py runserver

