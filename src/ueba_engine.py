import json
import pandas as pd
from sklearn.ensemble import IsolationForest

class ISPF_UEBA_Engine:
    def __init__(self):
        # 이상 탐지 모델 (비지도 학습)
        self.model = IsolationForest(contamination=0.05)
        self.risk_threshold = 80 # 위험 점수 임계치

    def load_data(self, filepath):
        with open(filepath, 'r') as f:
            self.data = json.load(f)
        self.df = pd.DataFrame(self.data)

    def calculate_risk_score(self, log):
        """
        ISPF-ITM 위험 평가 알고리즘 구현
        복합적인 요소를 고려하여 0~100의 위험 점수 산출
        """
        score = 0
        
        # 1. 행위 기반 이상 탐지 (Data Volume Anomaly)
        if log['data_volume_mb'] > 1000: # 1GB 이상
            score += 50
        
        # 2. 시간 기반 이상 탐지 (Time Anomaly)
        if log['hour'] < 7 or log['hour'] > 22: # 심야 시간
            score += 30
            
        # 3. 컨텐츠 기반 탐지 (DLP 연동)
        if 'content_tag' in log and log['content_tag'] == 'PII_DETECTED':
            score += 40
            
        # 4. 위협 인텔리전스/패턴 매칭 (Sabotage)
        if 'command' in log and 'rm -rf' in log['command']:
            score += 100 # 즉시 차단 필요
            
        return min(score, 100)

    def run_analysis(self):
        print(">>> [ISPF-ITM] Layer 4: Monitoring & Analysis Started...")
        detected_threats = []
        
        for log in self.data:
            risk_score = self.calculate_risk_score(log)
            
            # 위험 점수가 임계치를 넘으면 위협으로 간주
            if risk_score >= self.risk_threshold:
                alert = {
                    "alert_id": f"ALERT-{log['user_id']}-{log['timestamp']}",
                    "user": log['user_id'],
                    "risk_score": risk_score,
                    "activity": log.get('activity_type', 'UNKNOWN'),
                    "details": log
                }
                detected_threats.append(alert)
                
        return detected_threats