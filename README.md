ISPF-ITM: 기업 내부자 위협 관리를 위한 통합 보안 정책 프레임워크 (PoC)
Integrated Security Policy Framework for Insider Threat Management (ISPF-ITM)

본 리포지토리는 성균관대학교 정보통신대학원 정보보호학과 하헌재의 석사 학위 논문 **"기업 내부자 위협 관리를 위한 보안 정책 프레임워크: 효과성 분석 및 통합적 접근법"**에서 제안된 ISPF-ITM 프레임워크의 개념 증명(PoC: Proof of Concept) 코드를 포함하고 있습니다.

1. 로그 생성 및 시나리오 시뮬레이션 (log_generator.py)
정상 업무 패턴과 3가지 핵심 내부자 위협 시나리오(악의적 유출, 부주의, 사보타주)가 혼합된 가상 로그 데이터를 생성합니다.

2. 지능형 위협 탐지 (ueba_engine.py)
Monitoring Layer 구현: Isolation Forest 알고리즘과 룰셋을 결합하여 사용자 행위의 이상치(Anomaly)를 탐지하고 동적 위험 점수(Risk Score, 0~100)를 산출합니다.

3. 자동화된 대응 (soar_playbook.py)
Response Layer 구현: 산출된 위험 점수와 위협 유형에 따라 사전에 정의된 Playbook을 트리거하여, 계정 잠금, 차단, 경고 등의 조치를 자동 수행합니다.
