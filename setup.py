import sys
import subprocess
import os

REQUIRED_VERSION = (3, 10)
VENV_DIR = "arc_task_env"
REQUIREMENTS_FILE = "requirements.txt"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
EYETRACKER_WHL_PATH = os.path.join(SCRIPT_DIR, "psychopy_eyetracker_sr_research-0.0.5-py3-none-any.whl")

def check_python_version():
    """Python 버전이 맞는지 확인 (아니면 종료)"""
    if sys.version_info[:2] != REQUIRED_VERSION:
        print(f"[ERROR] Python {REQUIRED_VERSION[0]}.{REQUIRED_VERSION[1]} 버전에서만 실행 가능합니다.")
        print(f"현재 버전: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        sys.exit(1)

def create_virtualenv():
    """가상환경 생성 (없으면 새로 생성)"""
    if not os.path.exists(VENV_DIR):
        print(f"[INFO] 가상환경 생성 중... ({VENV_DIR})")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print(f"[INFO] 가상환경 '{VENV_DIR}' 이미 존재함.")

def install_requirements():
    """requirements.txt에 있는 패키지 설치"""
    pip_path = os.path.join(VENV_DIR, "Scripts", "pip") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "pip")
    
    print("[INFO] pip 업그레이드 중...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

    if os.path.exists(REQUIREMENTS_FILE):
        print(f"[INFO] {REQUIREMENTS_FILE}에 있는 패키지 설치 중...")
        subprocess.check_call([pip_path, "install", "-r", REQUIREMENTS_FILE])
    else:
        print(f"[WARNING] {REQUIREMENTS_FILE} 파일이 없습니다. 패키지 설치를 건너뜁니다.")

    # EyeLink용 PsychoPy 확장 모듈 설치 (.whl)
    if os.path.exists(EYETRACKER_WHL_PATH):
        print(f"[INFO] EyeLink PsychoPy 확장 모듈 설치 중 ({EYETRACKER_WHL_PATH})...")
        subprocess.check_call([pip_path, "install", EYETRACKER_WHL_PATH])
    else:
        print(f"[WARNING] EyeLink 휠 파일을 찾을 수 없습니다: {EYETRACKER_WHL_PATH}. 설치 건너뜁니다.")

if __name__ == "__main__":
    check_python_version()
    create_virtualenv()
    install_requirements()
    print("환경 세팅 완료")
    print("가상환경 활성화: {'arc_task_env\\Scripts\\activate' if os.name == 'nt' else 'source arc_task_env/bin/activate'}")