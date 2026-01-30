from google.genai import types
from openai import OpenAI
from google.adk.tools.tool_context import ToolContext
from typing import List, Dict, Any
import traceback  # 👈 오류 추적을 위해 추가

client = OpenAI()


async def generate_narrations(
    tool_context: ToolContext, voice: str, voice_instructions: List[Dict[str, Any]]
):
    """
    Generate narration audio for each scene using OpenAI TTS API
    """

    print("\n--- 🎙️ Voice Generator 시작 ---")
    existing_artifacts = await tool_context.list_artifacts()
    generated_narrations = []

    if not voice_instructions:
        print("[WARN] 'voice_instructions'가 비어있습니다. Voice Generator를 건너뜁니다.")
        # 👈 [수정] 빈 리스트라도 정상 종료되도록 수정
        return {
            "success": True,
            "narrations": [],
            "total_narrations": 0,
        }

    for instruction in voice_instructions:
        try:
            text_input = instruction.get("input")
            scene_id = instruction.get("scene_id")
            filename = f"scene_{scene_id}_narration.mp3"
            
            # 👈 [수정] instructions가 None일 경우를 대비
            instructions_raw = instruction.get("instructions", "")
            instructions_log = instructions_raw[:50] if instructions_raw else ""


            if filename in existing_artifacts:
                print(f"[INFO] 오디오 파일 {filename}이(가) 이미 존재하여 건너뜁니다.")
                generated_narrations.append(
                    {
                        "scene_id": scene_id,
                        "filename": filename,
                        "input": text_input,
                        "instructions": instructions_log,
                    }
                )
                continue

            # --- 1. OpenAI TTS API 호출 ---
            print(f"[INFO] 씬 {scene_id}의 오디오 파일 ({filename}) 생성 중...")
            with client.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice=voice,
                input=text_input
                # 'instructions' 파라미터는 API에 없으므로 제외
            ) as response:
                audio_data = response.read()

            # --- 2. 아티팩트 생성 및 저장 ---
            artifact = types.Part(
                inline_data=types.Blob(mime_type="audio/mpeg", data=audio_data)
            )

            await tool_context.save_artifact(filename=filename, artifact=artifact)
            print(f"[SUCCESS] 씬 {scene_id}의 오디오 파일 {filename} 저장 완료.")

            generated_narrations.append(
                {
                    "scene_id": scene_id,
                    "filename": filename,
                    "input": text_input,
                    "instructions": instructions_log,
                }
            )
        
        except Exception as e:
            # 👈 [수정] 오류가 발생해도 멈추지 않고 로그만 남기고 다음 씬으로 이동
            print(f"❌ [ERROR] 씬 {scene_id} 오디오 생성 실패: {e}")
            print(traceback.format_exc()) # 👈 더 자세한 오류 로그 출력
            continue # 다음 루프로 넘어감

    # --- 3. (확인) 'return' 문이 for 루프 밖에 있음 ---
    print(f"--- 🎙️ Voice Generator 종료: 총 {len(generated_narrations)}개의 오디오 처리 완료 ---")
    return {
        "success": True,
        "narrations": generated_narrations,
        "total_narrations": len(generated_narrations),
    }