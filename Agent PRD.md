Okay, here is the complete Product Requirements Document (PRD) for Project Insight, incorporating all the discussed refinements, including the detailed user inputs, the `o4-mini-high` base model, and the RAG-centric architecture.

---

**Product Requirements Document: College Admission Chances Agent (Project Insight)**

**1. Introduction**

*   **1.1 Purpose:** This document outlines the requirements for "Project Insight," an AI-powered agent designed to assist prospective college students, parents, and counselors in researching colleges and estimating the likelihood of admission to specific institutions. The agent will leverage the capabilities of the OpenAI Agents SDK (or compatible API like Responses API) to conduct deep research, analyze user profiles against institutional data, and provide personalized insights.
*   **1.2 Problem Statement:** The college application process is complex, stressful, and often opaque. Students struggle to identify suitable colleges, understand their specific admission requirements, and realistically assess their chances. Information is fragmented across various sources, and personalized guidance is often expensive or inaccessible.
*   **1.3 Proposed Solution:** Project Insight will act as a specialized research assistant. Users will provide their detailed academic profile, extracurricular activities, awards, preferences, and a specific list of target colleges. The agent, powered by **`o4-mini-high`**, a model explicitly designed for **complex reasoning and advanced agentic tool use**, and leveraging a specialized Retrieval-Augmented Generation (RAG) system containing curated college data, will analyze the user profile against institutional data primarily retrieved via RAG. It will utilize its inherent agentic capabilities to combine RAG retrieval with supplemental web searches as needed, providing a nuanced assessment of admission chances, supporting evidence, and contextual information, benefiting from the enhanced reasoning capacity of the `-high` variant.
*   **1.4 Scope:** This PRD covers the initial version (v1.0) of the agent, focusing on core research, analysis, and prediction functionalities for undergraduate admissions primarily within the United States, based on user-provided profile data and a target list of schools.

**2. Goals & Objectives**

*   **2.1 Primary Goal:** To provide users with a data-informed, personalized assessment of their admission chances to specific colleges, supported by relevant research findings retrieved primarily via a curated RAG system.
*   **2.2 Secondary Goals:**
    *   Streamline the college research process by consolidating information gathering using RAG and supplemental search.
    *   Identify potential "reach," "target," and "safety" schools based on user profile and historical data.
    *   Highlight key strengths and weaknesses of a user's profile relative to specific institutions.
    *   Provide context about admission factors beyond quantitative metrics (e.g., institutional priorities, program competitiveness) based on available data.
    *   Maintain transparency about data sources (RAG vs. Web), data freshness, and the probabilistic nature of predictions.

**3. Target Audience**

*   **3.1 Primary:** High school students (Sophomores, Juniors, Seniors) planning to apply to 4-year undergraduate programs in the US.
*   **3.2 Secondary:** Parents/Guardians of prospective students, High School Counselors, Independent Educational Consultants.

**4. Key Features (Functional Requirements)**

*   **4.1 User Profile Creation & Management:**
    *   **FR1:** Users must be able to input and securely store detailed academic profile information:
        *   **GPA:** Value, Scale (e.g., 4.0, 5.0, 100), Weighting (Weighted/Unweighted). Optionally, users can describe their GPA trend (e.g., upward, consistent).
        *   **Course Rigor:** Specific count of advanced courses taken (e.g., Number of AP courses, Number of IB courses, Number of Honors courses).
        *   **Standardized Test Scores:** SAT (Total, ERW, Math), ACT (Composite, individual sections), AP/IB exam scores. Users must be able to indicate if they intend to submit scores (reflecting test-optional policies).
    *   **FR2:** Users must be able to input qualitative and quantitative aspects of their profile:
        *   **Extracurricular Activities:** Provide a list of activities, including *detailed descriptions* covering role, responsibilities, duration, time commitment per week/year, and specific achievements or impact.
        *   **Awards & Honors:** List significant awards/honors with brief descriptions of their scope (e.g., school, regional, national) and significance.
        *   **Work Experience:** Similar descriptive detail as Extracurriculars.
        *   **Intended Major(s)/Areas of Interest:** Specify primary and potentially secondary academic interests.
    *   **FR3:** Users must be able to specify demographic information relevant to admissions (e.g., residency, first-generation status, legacy status - *Note: Handle with extreme sensitivity and clear purpose explanation*).
    *   **FR4:** Users should be able to save, view, and update their profile information.
*   **4.2 College Selection & Research:**
    *   **FR5:** Users must provide a **specific list** of target colleges for analysis in a given request. The agent's research and analysis for that interaction will be **scoped exclusively** to the schools on this provided list.
    *   **FR6:** The agent must retrieve relevant information about the specified colleges **primarily using its integrated RAG system**. This RAG system will contain curated data points including:
        *   General admission statistics (acceptance rate, SAT/ACT ranges, GPA ranges - primarily from Common Data Set and IPEDS).
        *   Program-specific information (where available and structured in the RAG).
        *   Summaries of stated institutional priorities, mission, and evaluation criteria.
        *   Key campus information (size, location, setting).
    *   **FR6a:** The agent **must utilize a web browsing tool agentically as a secondary measure** to search for information *not* found or potentially outdated in the RAG system. This includes:
        *   Very recent news or policy changes impacting admissions.
        *   Highly specific details about niche programs or faculty.
        *   Verification of critical data points if conflicting information arises or if instructed by the reasoning model.
    *   **FR7:** The RAG system serves as the **primary, pre-loaded knowledge base**, containing processed data from reliable sources.
*   **4.3 Admission Chance Analysis & Prediction:**
    *   **FR8:** The agent must compare the user's detailed profile data (including GPA, course rigor counts, test scores *if submitting*, qualitative EC/Award descriptions) against the data retrieved **primarily from the RAG system** (supplemented by web search as needed) for the **target colleges specified in the list (FR5)**.
    *   **FR9:** The agent must generate an estimated likelihood of admission, potentially categorized (e.g., High Likelihood/Safety, Likely/Target, Possible/Reach, Unlikely/Far Reach). *Crucially, this must be presented as an estimation based on available data, not a guarantee.*
    *   **FR10:** The agent, leveraging `o4-mini-high`'s reasoning, should provide a rationale for its assessment, highlighting:
        *   Comparison of user's quantitative metrics to the college's typical ranges (from RAG/web).
        *   *Plausible* alignment of user's described activities/awards with stated institutional priorities/values (based on RAG/web data). *(Requires careful interpretation by the model)*.
        *   User profile weaknesses or areas below the college's typical range.
        *   Specific factors likely to influence the decision (e.g., test-optional policy impact, stated importance of essays/ECs, residency preference, major competitiveness if data available).
        *   If any part of the rationale draws from forum/social media-derived insights, it must be explicitly stated and qualified (e.g., 'Some anecdotal discussions on public forums suggest...', 'Qualitative trends observed in online communities indicate...').
    *   **FR11:** The agent should perform comparative analysis *across the colleges provided in the user's list (FR5)*.
    *   **FR12 (Stretch Goal):** The agent could potentially use Code Interpreter agentically to perform statistical analysis on retrieved numerical data (e.g., percentile comparisons).
*   **4.4 Reporting & Interaction:**
    *   **FR13:** The agent must present the research findings and admission chance assessment in a clear, structured, and easily understandable format (e.g., a generated report within the chat interface).
    *   **FR14:** Users must be able to ask follow-up questions to clarify findings, request deeper dives into specific areas, or refine their profile/college list.
    *   **FR15:** The agent must cite its sources. For data points from the RAG, it should ideally indicate the underlying source and freshness date stored within the RAG (e.g., "Based on the 2023-24 Common Data Set via RAG,"). For web-retrieved data, it should cite the URL/source.
    *   **FR16:** The agent must include clear disclaimers about the limitations of the prediction (data gaps, qualitative factors, holistic review) and the probabilistic nature of college admissions.

**5. Non-Functional Requirements**

*   **5.1 Accuracy & Reliability:**
    *   **NFR1:** Predictions should be based primarily on the data within the RAG system, which must have a defined update cadence (e.g., annually for CDS/IPEDS data, potentially quarterly/monthly for key website elements). The agent must clearly state the perceived freshness of the RAG data used.
    *   **NFR1a:** A robust process for validating, ingesting, and updating data within the RAG system is critical and must be implemented and maintained. For forum/social media data, 'validation' will focus on the effectiveness of anonymization, adherence to ethical guidelines, and plausibility of extracted trends, rather than factual verification of individual data points.
    *   **NFR2:** The underlying logic for comparison and assessment, driven by `o4-mini-high`, should be consistent and grounded in established admission factors, while acknowledging model interpretation.
    *   **NFR3:** The agent service must be highly available, especially during peak application season (Aug-Jan).
*   **5.2 Performance:**
    *   **NFR4:** Research and analysis for a single college, relying primarily on fast RAG retrieval and the **`o4-mini-high`** model, should ideally complete within **45-120 seconds**. Latency needs monitoring as it represents a trade-off for enhanced reasoning. Interactions requiring supplemental web searches may take longer.
    *   **NFR5:** Basic conversational responses (acknowledgements, simple clarifications) should be near real-time.
*   **5.3 Security & Privacy:**
    *   **NFR6:** All user profile data must be stored securely and encrypted both at rest and in transit.
    *   **NFR7:** Compliance with relevant privacy regulations (e.g., COPPA if direct <13 marketing occurs - *avoid initially*, CCPA, GDPR if applicable) is mandatory. Clear privacy policy and terms of service are required. Strict PII scrubbing and ethical data handling protocols are paramount for any data sourced from public online discussions.
    *   **NFR8:** Anonymization or aggregation techniques should be considered for any internal analysis or model improvement using user data (if planned). Explicit user consent is required for data usage beyond direct service provision.
*   **5.4 Usability:**
    *   **NFR9:** The interface (likely conversational) should be intuitive and easy for the target audience to use.
    *   **NFR10:** Instructions and explanations provided by the agent should be clear, concise, and avoid excessive jargon.
*   **5.5 Maintainability & Scalability:**
    *   **NFR11:** The agent's prompts and **especially the RAG system's data ingestion and update pipelines** must be designed for efficient maintenance and updates.
    *   **NFR12:** The architecture (including the RAG system and API infrastructure) should be designed to handle a growing number of users and potentially colleges.

**6. Data Requirements & Sources**

*   **6.1 User-Provided Data:**
    *   Academic Metrics: GPA (Value, Scale, Weighting, Trend Description), Count of AP/IB/Honors Courses, Standardized Test Scores (SAT, ACT, AP, IB) & Submission Intent.
    *   Activities & Achievements: Detailed Descriptions of Extracurriculars (Role, Impact, Commitment), List/Descriptions of Awards/Honors, Work Experience Descriptions.
    *   Goals: Intended Major(s).
    *   Demographics: Residency, First-Gen Status, Legacy Status (Optional, Sensitive).
    *   **Target List:** A defined list of colleges for the specific analysis request.
*   **6.2 External Data Sources (For RAG Ingestion & Supplemental Search):**
    *   **Primary for RAG:** Common Data Sets (CDS), Integrated Postsecondary Education Data System (IPEDS), Key structured information scraped periodically from official college Admissions websites (e.g., stats pages, mission statements, stated evaluation criteria, program pages).
    *   **Primary for Supplemental Search:** Official College Admissions websites, reputable higher education news sources.
    *   **Secondary:** College Board/ACT aggregate reports, Niche/US News (used cautiously for qualitative context or stated priorities).
    *   **Tertiary/Supplemental (Experimental - Use with Extreme Caution & Transparency):** Potentially, anonymized and aggregated data points or qualitative trends extracted from publicly available, relevant online forums and social media discussions (e.g., specific subreddits, College Confidential).
        *   **Strict conditions:** Subject to rigorous ethical review, ToS compliance of source platforms, robust PII-scrubbing and anonymization techniques. Data will primarily be used for qualitative insights or to identify *potential* trends if reliable extraction and aggregation are feasible. Individual, unverified anecdotes will not be used as factual basis for predictions.
        *   **Transparency:** The agent must clearly label or qualify any information derived from such sources.
*   **6.3 Knowledge Base (RAG System - Central):** This is the core data repository.
    *   Contains structured and unstructured data extracted and indexed from sources in 6.2.
    *   Must include metadata for data source and freshness date for each key piece of information. The RAG system must clearly distinguish the provenance of data, especially for information sourced from forums/social media. This distinction must be usable by the agent to qualify its responses.
    *   Requires effective chunking, embedding strategies, and indexing optimized for college admission data types and queries.
*   **6.4 Data Limitations:** Acknowledge gaps in publicly available data (e.g., specific data by major, holistic review factors, unpublished internal cutoffs). Agent responses must reflect these uncertainties, even with RAG. Risk of stale data in RAG if updates fail. Data derived from forums/social media is inherently anecdotal, unverified, subject to significant self-selection bias, and may not be representative. It should be treated as qualitative and potentially indicative of trends at best, not as factual input equivalent to official data.

**7. Technology Stack**

*   **7.1 Core AI:** **Google Gemini 2.5 Flash** (leveraging its native search grounding, reasoning, and controllable thinking capabilities via Google's Gemini API/SDKs).
*   **7.2 Agent Tools:**
    *   **`Retrieval` (Primary):** Interfacing with the specialized RAG system (e.g., querying a vector database API like Pinecone, ChromaDB, etc.) orchestrated via LangChain or directly.
    *   **`Native Web Search` (Secondary/Supplemental):** Utilizing Gemini 2.5 Flash's built-in search grounding capabilities, invoked agentically by the model to find information not present or outdated in the RAG system.
    *   **`Code Interpreter` (Potential):** Agentic use of code execution capabilities (if supported by Gemini 2.5 Flash API, potentially via function calling or a native tool) for calculations if needed.
*   **7.3 Backend:** **Python** (likely using a web framework such as Flask or Django) will be the primary language. The agent itself will be developed using **Google's Agent Development Kit (ADK)** and its Python SDK to orchestrate interactions with Gemini 2.5 Flash (including its native tools like search), manage RAG pipelines, and handle agentic logic. Other libraries like LangChain may be used for specific sub-tasks (e.g., document processing for RAG) if deemed beneficial, but ADK will be the primary agent framework. The backend will also manage user state (session-based), API key security, and user database interactions (if any beyond session data).
*   **7.4 Database:**
    *   **User Data:** PostgreSQL, MySQL, or NoSQL DB (like MongoDB) for storing user profiles.
    *   **RAG Data:** Vector Database (e.g., Pinecone, Weaviate, ChromaDB, Milvus, PostgreSQL w/ pgvector) for storing and querying embeddings and source data.
*   **7.5 Frontend (If applicable):** Web interface (React, Vue, Angular) or integration into existing platforms (e.g., custom web app, educational portal).

**8. Success Metrics**

*   **8.1 User Engagement:**
    *   Number of active users, session frequency.
    *   Average number of colleges researched per user session.
    *   Session duration and interaction depth (number of follow-up questions).
*   **8.2 Task Completion:**
    *   Percentage of users successfully generating a comprehensive admission chance report for their listed schools.
    *   Frequency of supplemental web search usage (indicates RAG gaps or need for very recent info).
*   **8.3 User Satisfaction:**
    *   User feedback surveys/ratings (e.g., "How helpful and accurate was this assessment?").
    *   Qualitative feedback on clarity, reasoning quality, and perceived accuracy.
*   **8.4 Data Quality:**
    *   Regular audits of data within the RAG system for accuracy and freshness.
    *   Tracking of instances where web search contradicts or significantly updates RAG data.
*   **8.5 (Long Term/Difficult):** Correlation between agent assessments (e.g., safety/target/reach categorization) and actual user admission outcomes (requires ethical data collection with explicit user consent).

**9. Future Considerations (Post V1.0)**

*   **9.1 Enhanced Profile Input:** More granular course/grade input, potential for essay theme analysis (advanced NLP needed), recommendation letter context (user summaries).
*   **9.2 Financial Aid & Scholarship Research:** Adding RAG capabilities and agent skills for researching estimated costs, net price calculators, and relevant scholarships.
*   **9.3 International Student Support:** Expanding RAG data and profile options for non-US applicants and universities outside the US.
*   **9.4 Counselor Dashboard:** A specialized interface for counselors to manage multiple student profiles and reports.
*   **9.5 Model Refinement:** Evaluating newer OpenAI models or fine-tuning (if feasible and ethically sound) on relevant datasets.
*   **9.6 Integration:** API for integration into school counseling platforms or other EdTech tools.

**10. Open Questions & Risks**

*   **10.1 RAG Data Freshness & Coverage:** Ensuring the curated RAG data is consistently updated is paramount. How frequently will different data types be refreshed? What is the process for validating data before ingestion? How are gaps in the RAG handled effectively?
*   **10.2 Prediction Accuracy & Ethics:** Even with advanced models like Gemini 2.5 Flash, accurately modeling holistic review based on limited inputs and public data is challenging. Managing user expectations about the *estimate* nature is critical. Avoiding reinforcement of historical biases present in data sources is essential.
*   **10.3 Scalability & Cost:** Gemini 2.5 Flash API costs, plus the significant costs of building, hosting, embedding, and maintaining the specialized RAG system (vector DBs, data pipelines) need careful management.
*   **10.4 Tool Reliability:** Dependency on RAG system uptime/performance/accuracy and the reliability of Gemini 2.5 Flash's native search capabilities.
*   **10.5 Holistic Review Complexity:** Explicitly acknowledging the agent's limitations in assessing highly subjective factors (essays, interview quality, specific recommendation strength, institutional needs) is vital.
*   **10.6 Regulatory Compliance:** Ensuring ongoing compliance with data privacy laws (COPPA, CCPA, GDPR, etc.).
*   **10.7 RAG Maintenance Overhead:** The ongoing operational effort (monitoring sources, running pipelines, managing DB, ensuring quality) is significant.
*   **10.8 Performance vs. Capability Trade-off:** Validating that Gemini 2.5 Flash's latency (potentially managed via "controllable thinking") is acceptable for the user experience, given its reasoning capabilities and native search.
*   **10.9 Gemini 2.5 Flash Capabilities Verification:** Ensuring that the native search grounding of Gemini 2.5 Flash can be used truly agentically via API to meet FR6a, and verifying its reasoning and other tool integration capabilities in practice for Project Insight's specific needs.
*   **10.10 Use of Forum/Social Media Data:**
    *   Ethical and privacy concerns (PII handling, user expectations, ToS of platforms).
    *   Data reliability, verifiability, and potential for bias.
    *   Technical difficulty in accurately extracting, anonymizing, and structuring data.
    *   Risk of users misinterpreting agent insights derived from anecdotal sources.

---