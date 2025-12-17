class ISPF_SOAR_Playbook:
    def __init__(self):
        print(">>> [ISPF-ITM] Layer 5: Response System Initialized.")

    def execute_playbook(self, alert):
        """
        위협 유형 및 위험 점수에 따른 자동 대응 로직
        """
        risk_score = alert['risk_score']
        activity = alert['activity']
        user = alert['user']
        
        print(f"\n[!] ALERT RECEIVED: User={user}, Score={risk_score}, Type={activity}")

        # 대응 로직 (Scenario Mapping)
        
        # 시나리오 3: 시스템 파괴 시도 -> 즉시 계정 잠금 (Critical)
        if risk_score >= 90:
            self.action_lock_account(user)
            self.action_isolate_network(user)
            self.action_notify_ciso(alert)
            
        # 시나리오 1: 정보 유출 시도 -> 차단 및 관리자 통보 (High)
        elif risk_score >= 70 or activity == "DATA_EXFILTRATION":
            self.action_block_usb_port(user)
            self.action_revoke_cloud_access(user)
            self.action_notify_manager(alert)
            
        # 시나리오 2: 부주의한 실수 -> 경고 및 교육 (Medium)
        elif "CLOUD_UPLOAD" in activity:
            self.action_delete_public_link(alert['details'].get('file_path'))
            self.action_send_warning_popup(user)
            self.action_assign_training(user)

    # --- Action Simulation Methods ---
    def action_lock_account(self, user):
        print(f"    [ACTION] AD Account Locked for user: {user}")

    def action_isolate_network(self, user):
        print(f"    [ACTION] Network Access Control (NAC): Device Isolated.")

    def action_block_usb_port(self, user):
        print(f"    [ACTION] DLP Agent: USB Write Permission Revoked.")

    def action_send_warning_popup(self, user):
        print(f"    [ACTION] User Notification: 'Security Policy Violation Detected.'")

    def action_assign_training(self, user):
        print(f"    [ACTION] HR System: Security Awareness Training Assigned.")
        
    def action_notify_ciso(self, alert):
        print(f"    [REPORT] CISO Emergency SMS Sent: {alert['alert_id']}")

    def action_delete_public_link(self, filename):
        print(f"    [ACTION] CASB API: Public link removed for {filename}")
        
    def action_revoke_cloud_access(self, user):
        print(f"    [ACTION] Firewall: Blocked access to Dropbox/GoogleDrive.")
        
    def action_notify_manager(self, alert):
        print(f"    [REPORT] Email sent to Line Manager.")

# --- 메인 실행부 (통합 테스트) ---
if __name__ == "__main__":
    # 1. 로그 생성
    import log_generator
    log_generator.generate_mock_logs(100)
    
    # 2. UEBA 탐지 수행
    import ueba_engine
    engine = ueba_engine.ISPF_UEBA_Engine()
    engine.load_data('../data/simulation_logs.json')
    alerts = engine.run_analysis()
    
    print(f"\n>>> Analysis Complete. {len(alerts)} High-Risk Threats Detected.")
    
    # 3. SOAR 대응 수행
    soar = ISPF_SOAR_Playbook()
    for alert in alerts:
        soar.execute_playbook(alert)