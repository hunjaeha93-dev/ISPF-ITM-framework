import json
import random
from datetime import datetime, timedelta

# 시나리오별 로그 생성을 위한 설정
def generate_mock_logs(num_entries=1000):
    logs = []
    users = ["dev_user", "hr_user", "sys_admin", "normal_emp"]
    
    # 1. 정상 행위 (Normal Behavior) 생성
    for _ in range(num_entries):
        log = {
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(1, 10000))).isoformat(),
            "user_id": random.choice(users),
            "activity_type": "FILE_ACCESS",
            "data_volume_mb": random.randint(1, 10),
            "file_path": "/var/data/project_docs",
            "hour": random.randint(9, 18), # 업무 시간
            "status": "allow"
        }
        logs.append(log)

    # 2. 시나리오 1: 악의적 정보 유출 (High Volume, Encryption) [cite: 622]
    # 평소와 다른 대용량 다운로드 및 암호화 파일 생성
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_id": "dev_user_leaving",
        "activity_type": "DATA_EXFILTRATION",
        "data_volume_mb": 5000, # 비정상적 대용량 (5GB)
        "file_path": "/secure/db/customer_list.zip.enc", # 암호화된 파일
        "hour": 14,
        "device": "USB_Mass_Storage",
        "status": "allow" # 초기에는 허용됨 (DLP 차단 전)
    })

    # 3. 시나리오 2: 부주의한 노출 (Public Cloud Upload) [cite: 630]
    # 민감 정보(개인정보)를 공개 클라우드에 업로드
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_id": "hr_user_mistake",
        "activity_type": "CLOUD_UPLOAD",
        "data_volume_mb": 50,
        "file_path": "salary_report_2025.xlsx",
        "destination": "public_gdrive_link", # 공개 링크
        "content_tag": "PII_DETECTED", # 개인정보 식별됨
        "hour": 20, # 야근 중 실수
        "status": "allow"
    })

    # 4. 시나리오 3: 시스템 사보타주 (After-hours, Destructive) [cite: 641]
    # 업무 시간 외 접속 및 삭제 명령
    logs.append({
        "timestamp": datetime.now().isoformat(),
        "user_id": "sys_admin_angry",
        "activity_type": "SYSTEM_COMMAND",
        "command": "rm -rf /var/lib/vm_images/*", # 파괴적 명령어
        "hour": 3, # 새벽 3시 (비정상 시간)
        "status": "execute"
    })

    # 파일로 저장
    with open('../data/simulation_logs.json', 'w') as f:
        json.dump(logs, f, indent=4)
    print(f"Generated {len(logs)} logs including attack scenarios.")

if __name__ == "__main__":
    generate_mock_logs()