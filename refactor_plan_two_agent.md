# Refactoring Plan: Two-Agent Architecture for Project Insight

This document outlines the plan to refactor the Project Insight agent into a two-agent system: an `InternalCoordinatorAgent` for complex processing and an `PresenterAgent` for user-facing interaction and report generation.

## 1. Overall Architecture

The system will consist of:

*   **`PresenterAgent` (Root Agent):**
    *   This will be the new `root_agent`.
    *   It receives the initial user query.
    *   Its primary role is to call the `InternalCoordinatorAgent` as its main tool, passing the user query.
    *   It receives a structured text output from the `InternalCoordinatorAgent`.
    *   It parses this structured text and formats it into a polished, human-readable report for the end-user.
    *   It should not perform any complex reasoning or direct calls to `RAGAgent`, `SearchAgent`, or `CodingAgent`.

*   **`InternalCoordinatorAgent` (Worker Agent, Tool for PresenterAgent):**
    *   This agent encapsulates the existing complex multi-step logic for analyzing colleges.
    *   It uses `RAGAgent`, `SearchAgent`, and `CodingAgent` as its tools.
    *   It follows the detailed, robust workflow defined previously to process each college, including all internal trace statements for its own state management and for debugging.
    *   Its **final output** (after processing all colleges) will be a single, structured text block (defined below) that the `PresenterAgent` can easily parse.
    *   It will have the `maximum_remote_calls` configuration set high (e.g., 50).

*   **Specialist Agents (`RAGAgent`, `SearchAgent`, `CodingAgent`):**
    *   These remain as defined, serving as tools for the `InternalCoordinatorAgent`.
    *   Their instructions to return concise, single-string text outputs are critical.

## 2. Changes to `insight_agent/prompts.py`

### A. Rename `get_expanded_agent_instructions()`

*   The existing function `get_expanded_agent_instructions()` will be renamed to `get_internal_coordinator_instructions()`.

### B. Modify `get_internal_coordinator_instructions()`

*   **Phases I & II:** The detailed logic for initializing, processing each college sequentially (Steps A-G, including internal trace statements like `INTERNAL_TRACE: ...`, checklist management, and Golden Rules) will remain largely **unchanged**. This agent still needs to perform its complex internal reasoning.
*   **Phase III (Final Output Generation):** This section will be significantly modified. Instead of generating a human-readable report, the `InternalCoordinatorAgent` will be instructed to output its complete findings as a single, structured text block. All `INTERNAL_TRACE:` messages from earlier phases should NOT be part of this final structured output.

    **Target Structured Output Format for `InternalCoordinatorAgent`:**
    ```text
    INTERNAL_COORDINATOR_OUTPUT_START

    USER_PROFILE_SUMMARY_START
    [Summary of user's academic profile as understood by the coordinator. If data was missing from user, note it here, e.g., "User GPA: 3.8/4.0. SAT Score: 1450. ACT Score: Not Provided."]
    USER_PROFILE_SUMMARY_END

    OVERALL_ANALYSIS_NOTES_START
    [Optional: Any brief overall notes the coordinator has about the user's list or analysis, e.g., "User list contains several highly selective institutions."]
    OVERALL_ANALYSIS_NOTES_END

    // Repeat for each college analyzed
    COLLEGE_ANALYSIS_BLOCK_START
    COLLEGE_NAME: [Full College Name]
    CLASSIFICATION: [Reach/Target/Safety/Insufficient Data for Classification]
    KEY_COMPARATIVE_DATA_POINTS: [Concise list: e.g., User GPA: 3.8 vs. College Avg GPA: 3.9; User SAT: 1450 vs. College 75th percentile: 1520; College Acceptance Rate: 15%]
    DETAILED_RATIONALE: [Full rationale, including notes on data gaps or agent issues for this college. This should be multiple sentences.]
    DATA_SOURCES_SUMMARY: [e.g., Primary data from RAGAgent. Recent policy update via SearchAgent. GPA conversion by CodingAgent.]
    INTERNAL_PROCESSING_NOTES: [Brief summary of agent interactions for this college, e.g., "RAGAgent: Success. SearchAgent: Skipped - not needed. CodingAgent: Not needed."]
    COLLEGE_ANALYSIS_BLOCK_END

    QUALITATIVE_SECTION_CONTENT_START
    College admissions are often holistic and consider many factors beyond GPA and test scores, such as essays, recommendations, extracurricular activities, and individual circumstances. This analysis focuses primarily on academic statistical alignment.
    QUALITATIVE_SECTION_CONTENT_END

    LIMITATIONS_SECTION_CONTENT_START
    This analysis is based on the data available up to [Current Date Placeholder - actual date can be inserted by PresenterAgent or omitted] from automated agents and publicly accessible information. Admission statistics can change, and individual college policies may vary.
    LIMITATIONS_SECTION_CONTENT_END

    DISCLAIMER_SECTION_CONTENT_START
    This AI-generated report is for informational purposes only and should not be considered definitive professional admissions counseling or a guarantee of admission outcomes. Users are encouraged to consult official college websites and admissions counselors for the most current and personalized advice.
    DISCLAIMER_SECTION_CONTENT_END

    INTERNAL_COORDINATOR_OUTPUT_END
    ```
    *   The prompt will explicitly instruct the `InternalCoordinatorAgent` to conclude its entire operation by producing text in this exact format, containing all the collected and synthesized information.

### C. Create `get_presenter_agent_instructions()`

*   This new function will return the prompt for the `PresenterAgent`.
*   **Instructions for `PresenterAgent`:**
    ```text
    You are PresenterAgent, an AI assistant responsible for delivering a polished college admissions analysis report to the user.

    Your workflow is:
    1.  Receive the user's query (which will include their academic profile and list of colleges).
    2.  Invoke your primary tool, the `InternalCoordinatorAgent`, by passing the exact user query to it. The `InternalCoordinatorAgent` will perform all the detailed analysis and data gathering.
    3.  Await the response from `InternalCoordinatorAgent`. This response will be a structured text block starting with `INTERNAL_COORDINATOR_OUTPUT_START` and ending with `INTERNAL_COORDINATOR_OUTPUT_END`.
    4.  Carefully parse this entire structured text block to extract all the provided information: User Profile Summary, Overall Analysis Notes, and details for each `COLLEGE_ANALYSIS_BLOCK` (Name, Classification, Key Data, Rationale, Sources), plus the standard Qualitative, Limitations, and Disclaimer sections.
    5.  Format this extracted information into a clear, well-organized, human-readable report. The report should follow this structure:
        *   **Executive Summary (Optional but Recommended):** Use `OVERALL_ANALYSIS_NOTES_START` content if suitable.
        *   **User Profile Summary:** Use `USER_PROFILE_SUMMARY_START` content.
        *   **Detailed College-by-College Analysis:** For each college block received:
            *   **College Name:** [Full College Name]
            *   **Classification:** [Reach/Target/Safety/Insufficient Data for Classification]
            *   **Key Comparative Data:** [Present clearly]
            *   **Detailed Rationale:** [Present the full rationale]
            *   **(Optional) Data Sources Summary:** [Present clearly]
        *   **General Notes & Disclaimers:** Combine and present the content from `QUALITATIVE_SECTION_CONTENT_START`, `LIMITATIONS_SECTION_CONTENT_START`, and `DISCLAIMER_SECTION_CONTENT_START` sections in a readable way.
    6.  Your final output to the user MUST ONLY be this formatted report. Do NOT include any of the structured data markers (e.g., `INTERNAL_COORDINATOR_OUTPUT_START`, `COLLEGE_ANALYSIS_BLOCK_END`), `INTERNAL_PROCESSING_NOTES`, or any of your own processing commentary in the output to the user.
    7.  If the `InternalCoordinatorAgent` fails or returns an error or malformed/unparseable structured text, your response to the user should be a polite message like: "I encountered an issue while processing your request with my internal analysis system. Please try again later or rephrase your query."
    ```

## 3. Changes to `insight_agent/agent.py`

### A. `internal_coordinator_agent` Definition

*   The existing `project_insight_coordinator` agent will be renamed to `internal_coordinator_agent`.
*   Its `instruction` will be set using `get_internal_coordinator_instructions()`.
*   Its tools (`RAGAgent`, `SearchAgent`, `CodingAgent` via `AgentTool`) and its `generate_content_config` (with `maximum_remote_calls=50`) will remain unchanged.

### B. `presenter_agent` Definition

*   A new `Agent` instance will be defined:
    ```python
    presenter_agent = Agent(
        name="PresenterAgent",
        model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"), // Or a suitable model for presentation
        instruction=get_presenter_agent_instructions(),
        tools=[
            AgentTool(agent=internal_coordinator_agent) // Its only tool
        ]
        // No special generate_content_config likely needed, default AFC limit is fine for one call.
    )
    ```

### C. Update `root_agent` Alias

*   The line `root_agent = project_insight_coordinator` will be changed to:
    `root_agent = presenter_agent`

## 4. Testing Considerations

*   Test the `InternalCoordinatorAgent` in isolation first (if ADK allows easily running a non-root agent) to ensure it produces the structured output correctly.
*   Then test the full `PresenterAgent` flow.
*   The `PresenterAgent`'s ability to parse the structured text reliably will be key. The prompt guides it, but LLM parsing can sometimes be imperfect. The clearer and more consistent the `InternalCoordinatorAgent`'s structured output, the better.

This refactoring separates the complex internal "thinking" and multi-step processing from the final user-facing presentation, aiming for a more robust and maintainable system. 