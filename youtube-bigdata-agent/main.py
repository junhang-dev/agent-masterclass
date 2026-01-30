import pandas as pd
from dotenv import load_dotenv
import unicodedata
import os
from tqdm import tqdm

# --- [수정 1] Agent, Task 클래스를 직접 import 합니다. ---
from crewai import Crew, Agent, Task 
from crewai.project import CrewBase, agent, task, crew

import dotenv

dotenv.load_dotenv()

@CrewBase
class YoutubeContentAnalysisCrew:
    """유튜브 콘텐츠 분석을 위한 Crew 클래스"""
    @agent
    def keyword_strategy_analyst(self):
        # 'agents.yaml'의 'keyword_strategy_analyst' 설정을 사용하여 Agent 객체를 생성합니다.
        return Agent(config=self.agents_config['keyword_strategy_analyst'])

    @agent
    def guest_profiler(self):
        return Agent(config=self.agents_config['guest_profiler'])

    @task
    def keyword_extraction_task(self):
        # 'tasks.yaml'의 'keyword_extraction_task' 설정을 사용하여 Task 객체를 생성합니다.
        return Task(config=self.tasks_config['keyword_extraction_task'])

    @task
    def interviewer_identification_task(self):
        return Task(config=self.tasks_config['interviewer_identification_task'])

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=0
        )

if __name__ == "__main__":
    print("## 🤖 유튜브 콘텐츠 분석 Crew를 시작합니다.")
    print("----------------------------------------")

    # --- [수정 2] 파일 경로를 명확히 하기 위해 스크립트가 있는 디렉토리 기준으로 경로 설정 ---
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'final_youtube_data_perfect.csv')

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"❌ [오류] '{file_path}' 파일을 찾을 수 없습니다. 스크립트와 같은 폴더에 있는지 확인하세요.")
        exit()

    # 한글 자소 분리 현상 해결 (NFC 정규화)
    text_columns = ['title', 'ocr_text']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).apply(lambda x: unicodedata.normalize('NFC', x) if pd.notna(x) else x)
    
    analysis_crew = YoutubeContentAnalysisCrew().crew()
    results = []

    # tqdm을 사용하여 진행 상황을 시각적으로 표시 (테스트를 위해 10개만 실행)
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="콘텐츠 분석 진행률"):
        inputs = {
            'title': row['title'],
            'ocr_text': row['ocr_text']
        }
        
        result = analysis_crew.kickoff(inputs=inputs)
        
        # --- [수정된 부분] ---
        # .raw_output 대신 .raw를 사용하여 결과에 접근합니다.
        keywords = analysis_crew.tasks[0].output.raw
        interviewer = analysis_crew.tasks[1].output.raw

        results.append({
            'video_id': row['video_id'],
            'agent_keywords': keywords,
            'agent_interviewer': interviewer
        })
        
    # 결과 병합 및 저장
    results_df = pd.DataFrame(results)
    df_final = pd.merge(df, results_df, on='video_id', how='left')

    output_filename = 'final_data_with_agent_analysis.xlsx'
    output_path = os.path.join(script_dir, output_filename)
    df_final.to_excel(output_path, index=False, engine='openpyxl')

    print("\n----------------------------------------")
    print("## ✅ Crew 실행이 완료되었습니다!")
    print(f"최종 분석 결과가 '{output_path}' 파일로 저장되었습니다.")
    print("----------------------------------------")
    print(df_final[['title', 'agent_keywords', 'agent_interviewer']].head())