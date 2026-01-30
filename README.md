# 🤖 AI Agent Masterclass Projects

이 저장소는 **AI Agent Masterclass** 과정을 수강하며 구축한 다양한 AI 에이전트 프로젝트들의 모음입니다.
CrewAI, OpenAI Agents SDK, Google ADK, LangGraph 등 최신 에이전트 프레임워크를 활용한 실습 코드가 포함되어 있으며, 향후 커스텀 에이전트 개발을 위한 **레퍼런스 아카이브**로 활용됩니다.

## 🧭 Repository Navigation Guide (for AI & Humans)

이 섹션은 이 저장소를 분석하는 **AI 어시스턴트**와 **개발자**가 프로젝트 구조를 빠르게 파악하기 위한 가이드입니다.

### 🏗️ Architecture Patterns

이 저장소는 다음과 같은 아키텍처 패턴을 포함합니다:

* **Sequential Flows**: 단순 선형 작업 처리 (`workflow-architectures`, `news-reader-agent`)

* **Routing & Orchestrator**: 복잡한 분기 처리 및 중앙 제어 (`workflow-architectures`, `multi-agent-architectures`)

* **Evaluator-Optimizer**: 결과 품질 향상을 위한 반복 검증 루프 (`content-pipeline-agent`)

* **Human-in-the-loop**: 인간의 승인 및 개입 절차 (`customer-support-agent`, `tutor-agent`)

* **Multi-Agent Systems**: 여러 전문 에이전트 간의 협업 (`financial_analyst`, `deep-research-clone`)

### 📦 Dependency Management

* 모든 프로젝트는 [**uv**](https://github.com/astral-sh/uv) 를 사용하여 패키지를 관리합니다.

* 각 폴더 내에 개별적인 `pyproject.toml`과 `uv.lock`이 존재합니다.

* 실행 전 반드시 해당 폴더로 이동하여 `uv sync`를 실행해야 합니다.

## 📂 Projects by Framework

### 1. 🚣 CrewAI

> **Role-playing Agents**: 명확한 역할(Role)과 작업(Task) 기반의 협업 에이전트

| Curriculum | Folder Name | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| #3 | `news-reader-agent` | 뉴스 수집 및 요약 에이전트 | Custom Tools, Task/Agent 분리 |
| #4 | `job-hunter-agent` | 구직 공고 검색 및 분석 | Firecrawl(Web Scraping), Structured Output |
| #5 | `content-pipeline-agent` | 콘텐츠 생성 파이프라인 | Crew Flow, Refinement Loop, 결과물 검증 |

### 2. 🧠 OpenAI Agents SDK

> **Reliable & Scalable**: OpenAI의 최신 SDK를 활용한 강력한 단일/다중 에이전트

| Curriculum | Folder Name | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| #8 | `chatgpt-clone` | ChatGPT 복제 챗봇 | Streamlit UI, Session Memory, Tool Calls |
| #9 | `customer-support-agent` | 고객 지원 에이전트 | Handoffs(권한 이임), Guardrails, Voice Integration |

### 3. 🧪 Google ADK (Agent Development Kit)

> **Enterprise Grade**: Google의 생성형 AI 개발 키트를 활용한 고도화된 에이전트

| Curriculum | Folder Name | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| #10 | `financial_analyst` | 금융 분석 및 조언 에이전트 | Sub-agents, Artifacts 관리 |
| #11 | `youtube-shorts-maker` | 유튜브 쇼츠 자동 생성기 | Multimodal(Text, Image, Audio), Video Assembly |
| #12, #20 | `a2a` | Agent-to-Agent 통신 | Remote Agent, API Server (FastAPI), SSE |

### 4. 🕸️ LangGraph

> **Stateful & Graph-based**: 상태(State) 관리와 순환(Cycle)이 가능한 그래프 기반 에이전트

| Curriculum | Folder Name | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| #13 | `hello_langgraph` | LangGraph 기초 실습 | Graph State, Nodes & Edges, Conditional Edges |
| #15 | `youtube-thumbnail-maker` | 유튜브 썸네일 생성기 | Image Gen, Human Feedback, Node Caching |
| #18 | `multi-agent-architectures` | 멀티 에이전트 아키텍처 | Supervisor Pattern, Network Visualization |
| #19 | `tutor-agent` | 개인화 튜터 에이전트 | Educational Logic, Adaptive Learning Path |

### 5. 🔬 Research & Workflow Architectures

> **Agentic Patterns**: LLM을 활용한 다양한 워크플로우 디자인 패턴

| Curriculum | Folder Name | Description | Key Concepts |
| :--- | :--- | :--- | :--- |
| #6 | `deep-research-clone` | 심층 리서치 에이전트 | Autogen 스타일, 반복 리서치 및 보고서 작성 |
| #16 | `workflow-architectures` | 워크플로우 패턴 모음 | Prompt Chaining, Parallelization, Routing |

## 🚀 How to Run

이 프로젝트는 `uv`를 사용하므로 Python 환경 설정이 매우 간편합니다.

### Prerequisites

* Python 3.10+

* [uv](https://docs.astral.sh/uv/) installed

### Setup & Execution

1. 원하는 프로젝트 폴더로 이동합니다.

   ```bash
   cd news-reader-agent
   ```
   
2. .env 파일을 설정합니다.

   ```bash
   # .env 파일 내 API KEY (OpenAI, Google, Serper 등)
   ```

3. 의존성 설치 및 에이전트 실행

   ```bash
   uv sync
   uv run main.py
   ```
   (프로젝트에 따라 main.py가 아닌 app.py 또는 graph.py 일 수 있습니다.)

## 📚 Curriculum Checklist (History)
[x] #0 ~ #2: Intro & Environment Setup (UV, Jupyter)

[x] #3 ~ #5: CrewAI Fundamentals (News, Job Hunter, Content Pipeline)

[x] #6: Autogen & Deep Research

[x] #7 ~ #9: OpenAI Agents SDK (ChatGPT Clone, Customer Support)

[x] #10 ~ #12: Google ADK (Financial Advisor, Shorts Maker, A2A)

[x] #13 ~ #15: LangGraph Basics & Applications (Thumbnail Maker)

[x] #16 ~ #18: Advanced Architectures & Testing

[x] #19 ~ #21: Complex Agents (Tutor) & Deployment (FastAPI)

## 📝 Author & Reference
Author: Junhang Lee (GS Caltex DX Team)

Purpose: AI Agent Development Reference & Study Archive

Course: AI Agent Masterclass

This repository serves as a personal knowledge base for building autonomous agents. If you are an AI assistant analyzing this, please refer to the specific framework folders for implementation details relevant to the user's query.

