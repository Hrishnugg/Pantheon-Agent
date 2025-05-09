# Implementation Plan: Project Insight (College Admission Chances Agent)

This document outlines the phased implementation plan for Project Insight, based on the Product Requirements Document (PRD).

**Overall Approach:**

We will follow an iterative development approach, focusing on delivering core functionality in early phases and progressively adding features and refinements. Each phase will include design, development, testing, and review.

---

**Phase 1: Foundation, Core RAG Setup, and Initial Data Ingestion**

*   **Duration:** (Estimate, e.g., 4-6 weeks)
*   **Goal:** Establish the foundational infrastructure, set up the core RAG system with initial data, and enable basic querying capabilities.

*   **Tasks & Deliverables:**
    1.  **Project Setup & Environment Configuration:**
        *   Deliverable: Git repository initialized with project structure.
        *   Deliverable: Python virtual environment and `requirements.txt` (or `pyproject.toml` with Poetry/PDM) for dependencies.
        *   Deliverable: Docker setup (if planned early for development consistency).
    2.  **Technology Stack Finalization & Setup:**
        *   Task: Confirm specific Python web framework (e.g., Flask, FastAPI).
        *   Task: Determine if any persistent storage (beyond RAG Vector DB) is needed for V1 (e.g., for operational logging). For V1, persistent user profiles and associated databases are out of scope.
        *   Task: Select and set up the Vector Database for RAG (e.g., ChromaDB, Pinecone - PRD 7.4).
        *   Task: Obtain and thoroughly review the API contract specifications from the frontend team to ensure backend compatibility.
        *   Deliverable: All chosen databases and frameworks installed and configured for development; API contract understood.
    3.  **Core AI Model & Agent Framework Integration Planning (Gemini 2.5 Flash + Google ADK):**
        *   Task: Deep dive into Google Gemini 2.5 Flash API documentation and **Google's Agent Development Kit (ADK)** documentation.
        *   Task: Focus on practical integration using ADK for: agentic search (Gemini native), controllable thinking, other tool use (e.g., Code Interpreter), RAG pipeline orchestration within ADK, and conversational memory management.
        *   Task: Outline specific ADK components, API calls, SDK usage, and architectural patterns for Project Insight.
        *   Task: Secure API access (Gemini) and set up Google Cloud project configurations for ADK and Gemini.
        *   Deliverable: Detailed integration plan for Gemini 2.5 Flash with Google ADK; API keys secured; development environment configured for Gemini & ADK SDKs.
    4.  **RAG - Data Source Identification & Initial Acquisition (Curated Subset):**
        *   Task: Identify and obtain initial samples of Common Data Sets (CDS), IPEDS, and key college website information (PRD 6.2) for a limited set of pilot colleges.
        *   Task: Conduct an initial ethical and feasibility review for potentially using anonymized data from 1-2 selected public forums (e.g., specific subreddits, as per PRD 6.2 Tertiary source definition). Assess ToS implications and PII handling challenges. This is exploratory for V1.
        *   Deliverable: Sample datasets (CDS, IPEDS, websites) acquired and stored; Initial ethical/feasibility report on forum data exploration.
    5.  **RAG - Data Ingestion Pipeline (v0.1 - Manual/Scripted):**
        *   Task: Develop initial document loaders (potentially using LangChain components if ADK's native capabilities are less suited for specific formats, or using ADK's RAG features directly) for the acquired *primary and secondary* data formats.
        *   Task: Implement initial text splitting/chunking strategy (again, ADK native or LangChain components) for primary/secondary data.
        *   Task: Integrate an embedding model (compatible with ADK/Gemini ecosystem) and develop scripts to process and load initial primary/secondary data into the Vector DB.
        *   Task (Conditional on positive feasibility review from Task 4 & V1 scope decision): Develop prototype scrapers/APIs for selected forums (if compliant and ethical) and an initial NLP pipeline for PII scrubbing, anonymization, and basic data point extraction from forum data. This is a high-risk, experimental component for V1.
        *   Deliverable: Initial primary/secondary data processed, embedded, and indexed in the Vector DB; Scripts for the v0.1 ingestion pipeline for this data, designed for compatibility with ADK's RAG approach; If pursued, prototype forum data ingestion/anonymization scripts and assessment of viability.
    6.  **RAG - Basic Retrieval Mechanism (within ADK or integrated):**
        *   Task: Implement a basic retrieval function to query the Vector DB, preferably using ADK's built-in RAG orchestration capabilities. If LangChain is used for RAG data prep, ensure seamless integration with ADK.
        *   Deliverable: A Python module/ADK component capable of retrieving relevant document chunks for the agent.
    7.  **Core AI - Agent Shell with Google ADK & Gemini 2.5 Flash:**
        *   Task: Securely set up API access to Gemini 2.5 Flash within the ADK environment (as per Task 3 deliverables).
        *   Task: Create a basic agent structure using **Google's Agent Development Kit (ADK)** that can:
            *   Take a user query.
            *   Utilize ADK to manage interaction flow and memory.
            *   Combine query with retrieved RAG context (via ADK's RAG features).
            *   Agentically invoke Gemini 2.5 Flash's native search tool (via ADK tool use).
            *   Get a response from Gemini 2.5 Flash, orchestrated by ADK.
        *   Deliverable: A simple ADK-based agent demonstrating basic interaction with Gemini 2.5 Flash, RAG context, and native search invocation.

---

**Phase 2: Session-Based User Input Handling & Core Agent Logic**

*   **Duration:** (Estimate, e.g., 4-6 weeks - potentially shorter due to removal of custom search tool dev)
*   **Goal:** Develop the core agent logic for accepting session-based user inputs through a multi-step UI and analyzing these inputs against college data from RAG, leveraging Gemini 2.5 Flash.

*   **Tasks & Deliverables:**
    1.  **Session-Based User Input - Data Structure Definition:**
        *   Task: Define the in-memory data structures and flow for capturing user inputs progressively through a multi-step UI within a single session (guided by PRD 4.1, 6.1 for data points).
        *   Deliverable: Documented data structures and UI flow for session-based user inputs.
    2.  **Session Data Handling & Security (No Persistent User Profiles for V1):**
        *   Task: Ensure secure handling of user input data during a session (encryption in transit for API calls - NFR6). Data at rest for user profiles is not applicable for V1.
        *   Task: Determine and implement strategy for managing user inputs collected across multiple steps within a single session (e.g., temporarily in-memory on the server, or passed between client/server).
        *   Task: Ensure no PII from session inputs is inadvertently persisted beyond the active session.
        *   Deliverable: Secure mechanisms for handling multi-step session-based user data; documentation on session data management.
    3.  **Agent Logic - Session Input Aggregation & Parsing:**
        *   Task: Develop mechanisms for the agent to aggregate and parse all user-provided data collected throughout the multi-step UI for a given session (GPA, course rigor, test scores, ECs, awards, etc. - PRD 4.1).
        *   Deliverable: Agent functions for processing structured and qualitative user inputs.
    4.  **Agent Logic - Integrating RAG for College Data:**
        *   Task: Integrate the RAG retrieval mechanism (from Phase 1) into the agent flow to fetch college-specific data based on user's target colleges (PRD FR5, FR6, FR8).
        *   Deliverable: Agent can dynamically pull relevant college info from RAG.
    5.  **Agent Logic - Profile-College Comparison (Initial):**
        *   Task: Develop initial logic (prompt engineering for Gemini 2.5 Flash) to compare user's quantitative metrics (GPA, test scores) against college data from RAG (PRD FR8, FR10).
        *   Task: Initial approach for Gemini 2.5 Flash to consider qualitative aspects (ECs, awards) against stated institutional priorities (PRD FR10).
        *   Deliverable: Agent can perform a basic comparison and identify matches/gaps.
    6.  **Agent Logic - Admission Chance Estimation (Categorized v0.1):**
        *   Task: Implement logic for the agent (guided by Gemini 2.5 Flash) to generate an initial categorized admission likelihood (e.g., Safety, Target, Reach - PRD FR9). This will be highly iterative.
        *   Deliverable: Agent can output a preliminary, categorized chance estimation.
    7.  **Agent Logic - Rationale Generation (v0.1):**
        *   Task: Prompt Gemini 2.5 Flash to provide a basic rationale for its assessment, highlighting key comparison points (PRD FR10).
        *   Deliverable: Agent provides a simple textual explanation for its estimation.

---

**Phase 3: Backend API Development, Reporting, and Iterative Refinement**

*   **Duration:** (Estimate, e.g., 4-6 weeks)
*   **Goal:** Develop the backend API to integrate with the existing frontend, implement reporting features, and refine agent performance.

*   **Tasks & Deliverables:**
    1.  **Backend API Development for Frontend Integration:**
        *   Task: Develop robust and well-documented API endpoints according to the established contract with the frontend team. This API will handle receiving user inputs collected by the frontend (session data) and returning agent research/predictions.
        *   Deliverable: Deployed backend API endpoints, tested for compatibility with the frontend's expected request/response formats.
    2.  **Reporting - Structured Output:**
        *   Task: Design and implement the presentation of research findings and admission chance assessment in a clear, structured format (PRD FR13).
        *   Deliverable: Agent outputs results in a well-organized report within the interface.
    3.  **Reporting - Source Citation:**
        *   Task: Implement mechanisms to cite data sources: RAG (including freshness date from metadata) and web URLs (PRD FR15).
        *   Deliverable: Reports include source citations.
    4.  **Reporting - Disclaimers:**
        *   Task: Integrate clear disclaimers about prediction limitations (PRD FR16).
        *   Deliverable: Disclaimers are prominently displayed with results.
    5.  **Interaction - Follow-up Questions (API Support):**
        *   Task: Ensure the backend API can support follow-up questions and maintain conversational context as required by the frontend's design (PRD FR14).
        *   Deliverable: API endpoints capable of handling conversational state for follow-up interactions.
    6.  **Refinement - RAG System & Agent Prompts:**
        *   Task: Test and refine RAG retrieval (chunking, embeddings, query construction) based on observed performance.
        *   Task: Iteratively refine prompts for Gemini 2.5 Flash to improve reasoning, rationale quality, and accuracy of estimations.
        *   Deliverable: Improved RAG relevance and agent response quality.
    7.  **Refinement - Data Ingestion Pipeline (v0.2 - Automation improvements):**
        *   Task: Enhance the data ingestion pipeline for better automation and handling of data updates for the initial set of colleges.
        *   Deliverable: More robust data ingestion scripts/tools.

---

**Phase 4: Advanced Features, Comprehensive Testing, & Deployment Preparation**

*   **Duration:** (Estimate, e.g., 6-8 weeks)
*   **Goal:** Implement remaining core features, conduct thorough testing, and prepare for initial deployment.

*   **Tasks & Deliverables:**
    1.  **Feature - Comparative Analysis Across Colleges:**
        *   Task: Implement agent logic to perform comparative analysis across the user's list of target colleges (PRD FR11).
        *   Deliverable: Agent can highlight differences and similarities between colleges in its report.
    2.  **Feature - RAG Data Update Strategy & Automation (NFR1a):**
        *   Task: Design and implement a strategy for regularly updating RAG data (e.g., annually for CDS, more frequently for website scrapes).
        *   Task: Automate parts of the RAG update process.
        *   Deliverable: Documented data update strategy and initial automation scripts.
    3.  **Stretch Goal - `Code Interpreter` Integration (If pursued for V1):**
        *   Task: Investigate and implement specific use cases for `Code Interpreter` (e.g., statistical analysis - PRD FR12), if deemed high-value for v1.0.
        *   Deliverable: `Code Interpreter` tool integrated and used agentically.
    4.  **Testing - Unit & Integration Tests:**
        *   Task: Develop comprehensive unit tests for all backend modules (agent logic, RAG components, API endpoints).
        *   Task: Develop integration tests for interactions between components (e.g., Agent-RAG, Agent-DB).
        *   Deliverable: High test coverage for core functionality.
    5.  **Testing - End-to-End (E2E) User Scenarios:**
        *   Task: Define and execute E2E tests covering common user workflows.
        *   Deliverable: E2E tests passing.
    6.  **NFR - Performance Testing & Optimization:**
        *   Task: Conduct performance tests for key operations (profile analysis, report generation) to meet NFR4 (45-120s target).
        *   Task: Identify and address performance bottlenecks.
        *   Deliverable: Performance test results and optimizations implemented.
    7.  **NFR - Security Hardening & Privacy Review:**
        *   Task: Conduct a security review of user data handling, API endpoints, and dependencies (NFR6, NFR7).
        *   Task: Implement any necessary security hardening measures.
        *   Deliverable: Security review report and fixes.
    8.  **Deployment - Strategy & Infrastructure Setup:**
        *   Task: Define the deployment strategy (e.g., Docker containers, serverless, PaaS).
        *   Task: Set up staging and production environments.
        *   Deliverable: Documented deployment plan and configured environments.
    9.  **Documentation - Initial Technical & User Guides:**
        *   Deliverable: Drafts of technical documentation for developers.
        *   Deliverable: Initial user guide for interacting with the agent.

---

**Phase 5: Initial Deployment, Monitoring, & Iteration**

*   **Duration:** (Ongoing)
*   **Goal:** Deploy v1.0, monitor its performance and usage, gather user feedback, and plan for subsequent iterations.

*   **Tasks & Deliverables:**
    1.  **Deployment - v1.0 Launch:**
        *   Task: Deploy the application to the production environment.
        *   Deliverable: Project Insight v1.0 is live.
    2.  **Monitoring - Setup & Activation:**
        *   Task: Implement and activate logging for key agent events, API calls, errors, and RAG performance.
        *   Task: Set up basic monitoring dashboards for system health and usage metrics (NFR3, Success Metrics 8.1, 8.2).
        *   Deliverable: Logging and monitoring systems are active.
    3.  **Feedback - User Acceptance Testing (UAT) & Initial Feedback Collection:**
        *   Task: Conduct UAT with a small group of target users (PRD 3).
        *   Task: Establish channels for collecting user feedback (surveys, direct feedback - Success Metric 8.3).
        *   Deliverable: UAT report and initial user feedback collated.
    4.  **Maintenance - RAG Data Quality & Freshness Monitoring (NFR1, NFR1a):**
        *   Task: Establish a process for regularly auditing RAG data quality and freshness.
        *   Deliverable: RAG data monitoring plan.
    5.  **Iteration - Backlog Grooming & v1.1 Planning:**
        *   Task: Analyze user feedback, performance data, and RAG effectiveness.
        *   Task: Prioritize bug fixes, improvements, and features for the next iteration (referencing PRD Section 9: Future Considerations).
        *   Deliverable: Prioritized backlog for v1.1. 