from ultralytics import YOLO
import csv
import cv2
from time import sleep
from requests import *

# YOLOv8 모델 불러오기
model = YOLO('yolov8n.pt')

# CSV 파일 생성
csv_filename = "motor_tracking.csv"
with open(csv_filename, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["frame", "x_center", "y_center", "width", "height", "motor1", "motor2"])

# 실시간 웹캠 입력
cap = cv2.VideoCapture(0)

# 카메라 중심 좌표 계산 (640x480 기준)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
center_x = frame_width // 2
print(f"📸 카메라 중심 X 좌표: {center_x}")

initial_area = None  # 초기 박스 넓이 저장 변수
frame_idx = 0

# 실시간 감지
for r in model(source=0, stream=True, show=True, conf=0.6, verbose=False, max_det=1):
    boxes = r.boxes
    motor1, motor2 = 0, 0  # 기본값(정지)

    if boxes is not None and len(boxes) > 0:
        box = boxes[0]  # 첫 번째 감지된 객체(사람)
        x_center, y_center, w, h = box.xywh[0].tolist()
        area = w * h  # 박스 넓이

        # 초기 박스 넓이 저장
        if initial_area is None:
            initial_area = area
            print(f"🎯 초기 박스 넓이 저장: {initial_area:.2f}")

        # --- 1번 모터 제어 (좌우 방향) ---
        diff_x = x_center - center_x
        if diff_x < -45:  # 카메라 중심보다 왼쪽
            motor1 = -1  # 반시계 방향
        elif diff_x > 45:  # 카메라 중심보다 오른쪽
            motor1 = 1   # 시계 방향
        else:
            motor1 = 0   # 정지

        # 결과 전송
        ip = "11.190.50.37"
        url = f"http://{ip}:8000/phymo?motor={motor1}"
        response = get(url)
        sleep(0.01)


    frame_idx += 1

cap.release()
cv2.destroyAllWindows()
