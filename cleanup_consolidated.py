import os

# 통합으로 인해 삭제할 파일
files_to_delete = [
    # 통합된 파일들
    "constants.py",  # → config.py로 통합
    "rules.py",      # → config.py로 통합
    "voice_handler.py",  # → voice.py로 이름 변경
    
    # 테스트/임시 파일들
    "cleanup.bat",
    "cleanup_files.py",
    "cleanup_consolidated.py",  # 자기 자신도 삭제
]

print("=" * 60)
print("파일 통합 후 정리 작업")
print("=" * 60)

deleted = []
not_found = []

for filename in files_to_delete:
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            deleted.append(filename)
            print(f"✅ 삭제: {filename}")
        except Exception as e:
            print(f"❌ 삭제 실패 {filename}: {e}")
    else:
        not_found.append(filename)
        print(f"⚠️  파일 없음: {filename}")

print("\n" + "=" * 60)
print(f"삭제 완료: {len(deleted)}개")
print(f"찾을 수 없음: {len(not_found)}개")
print("=" * 60)

print("\n✅ 통합 완료! 새로운 파일 구조:")
print("  - config.py (constants.py + rules.py)")
print("  - voice.py (voice_handler.py)")
print("  - 나머지 파일은 그대로 유지")
