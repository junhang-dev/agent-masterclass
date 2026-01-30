import os
import io
from google import genai
from google.genai import types
from google.adk.tools.tool_context import ToolContext

# --- .env에서 Google API 키 로드 및 설정 ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")

# --- Google GenAI 클라이언트 생성 ---
client = genai.Client(api_key=GOOGLE_API_KEY)

async def generate_images(tool_context: ToolContext):

    prompt_builder_output = tool_context.state.get("prompt_builder_output")
    optimized_prompts = prompt_builder_output.get("optimized_prompts")

    existing_artifacts = await tool_context.list_artifacts()

    generated_images = []

    for prompt in optimized_prompts:
        scene_id = prompt.get("scene_id")
        enhanced_prompt = prompt.get("enhanced_prompt")
        filename = f"scene_{scene_id}_image.jpeg"

        if filename in existing_artifacts:
            # 👈 [수정 1] AttributeError 해결을 위해 print()로 변경
            print(f"[INFO] 이미지 {filename}가 이미 존재하여 건너뜁니다.")
            
            generated_images.append(
                {
                    "scene_id": scene_id,
                    "prompt": enhanced_prompt[:100],
                    "filename": filename,
                }
            )
            continue

        # --- 1. Google Imagen 4.0 호출 ---
        try:
            response = client.models.generate_images(
                model='imagen-4.0-generate-001',
                prompt=enhanced_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="9:16",
                )
            )
            
            # 👈 [확인] 노트북에서 성공한 로직 (response.generated_images[0].image.image_bytes)
            generated_image_obj = response.generated_images[0]
            image_bytes = generated_image_obj.image.image_bytes

        except Exception as e:
            # 👈 [수정 1] AttributeError 해결을 위해 print()로 변경
            print(f"[ERROR] Google 이미지 생성 중 오류 발생 (Scene: {scene_id}): {e}")
            continue
        
        # --- 2. 아티팩트 저장 ---
        # (image_bytes가 올바르게 추출되었다면, 이 부분은 정상 동작해야 합니다)
        artifact = types.Part(
            inline_data=types.Blob(
                mime_type="image/jpeg",
                data=image_bytes,
            )
        )

        await tool_context.save_artifact(
            filename=filename,
            artifact=artifact,
        )

        generated_images.append(
            {
                "scene_id": scene_id,
                "prompt": enhanced_prompt[:100],
                "filename": filename,
            }
        )

    # --- 3. (버그 수정) return 문을 for 루프 밖으로 이동 ---
    return {
        "total_images": len(generated_images),
        "generated_images": generated_images,
        "status": "complete",
    }