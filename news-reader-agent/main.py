import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool, scrape_tool


@CrewBase
class NewsReaderAgent:

    @agent
    def news_hunter_agent(self):
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool],
        )

    @agent
    def summarizer_agent(self):
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[
                scrape_tool,
            ],
        )

    @agent
    def curator_agent(self):
        return Agent(
            config=self.agents_config["curator_agent"],
        )

    @agent
    def storyteller_agent(self):
        return Agent(
            config=self.agents_config['storyteller_agent'],
        )
    
    @agent
    def translator_agent(self):
        return Agent(
            config=self.agents_config['translator_agent'],
        )

    @agent
    def infographic_designer_agent(self):
        return Agent(
            config=self.agents_config['infographic_designer_agent'],
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"],
        )

    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"],
            context=[self.content_harvesting_task()]
        )

    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"],
            context=[self.summarization_task()]
        )
    
    @task
    def storytelling_task(self):
        return Task(
            config=self.tasks_config['storytelling_task'],
            context=[self.final_report_assembly_task()]
        )
    
    @task
    def translation_task(self):
        return Task(
            config=self.tasks_config['translation_task'],
            context=[self.storytelling_task()]
        )
    
    @task
    def infographic_creation_task(self):
        return Task(
            config=self.tasks_config['infographic_creation_task'],
            context=[self.translation_task()]
        )

    @crew
    def crew(self):
        return Crew(
            tasks=self.tasks,
            agents=self.agents,
            verbose=True,
        )

if __name__ == "__main__":
    print("## Welcome to the News Infographic Crew!")
    print("-----------------------------------------")
    inputs = {
        'topic': 'The Federal Reserve next interest rate move and its impact on US housing affordability in Fall 2025'
    }
    print(f"🤖 Starting analysis for topic: \"{inputs['topic']}\"")
    print("-----------------------------------------")

    # Crew를 초기화하고 실행합니다.
    news_crew = NewsReaderAgent().crew()
    result = news_crew.kickoff(inputs=inputs)

    # 최종 결과 요약 메시지를 출력합니다.
    print("\n-----------------------------------------")
    print("## ✅ Crew execution completed!")
    print("-----------------------------------------")
    print("All tasks have been successfully executed.")
    print("You can find the final outputs in the 'output' directory:")
    print(f"   - Final Report (Markdown): output/final_report.md")
    print(f"   - Final Infographic (HTML): output/final_infographic.html")