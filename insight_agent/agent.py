import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import google_search, built_in_code_execution
from google.adk.tools.agent_tool import AgentTool # Import AgentTool
from google.genai import types as genai_types # Import genai_types
# Import for RAG tool
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag # Ensure this is the correct import for RagResource

# Import prompts
from .prompts import get_internal_coordinator_instructions, get_presenter_agent_instructions

# Load environment variables from .env file
load_dotenv()

# --- Environment Variable Checks (Optional but Recommended) ---
# You can add checks here to ensure necessary variables are set, e.g.:
# if os.getenv("GOOGLE_GENAI_USE_VERTEXAI") == "TRUE":
#     if not os.getenv("GOOGLE_CLOUD_PROJECT"):
#         raise ValueError("GOOGLE_CLOUD_PROJECT not set in .env for Vertex AI")
#     if not os.getenv("GOOGLE_CLOUD_LOCATION"):
#         raise ValueError("GOOGLE_CLOUD_LOCATION not set in .env for Vertex AI")
#     if not os.getenv("RAG_CORPUS"):
#         raise ValueError("RAG_CORPUS not set in .env for Vertex AI RAG")
# else:
#     if not os.getenv("GOOGLE_API_KEY"):
#         raise ValueError("GOOGLE_API_KEY not set in .env for Google AI Studio")
# --- End Environment Variable Checks ---

# --- Specialist Agents Definition ---

# 1. RAG Agent (using existing vertex_rag_retrieval_tool)
vertex_rag_retrieval_tool = VertexAiRagRetrieval(
    name='retrieve_rag_documentation',
    description=(
        'Use this tool to retrieve specific documentation and data about US colleges from the specialized RAG corpus. '
        'This includes admission statistics, program details, course requirements, and other factual college-specific information.'
    ),
    rag_resources=[
        rag.RagResource(rag_corpus=os.environ.get("RAG_CORPUS"))
    ] if os.environ.get("RAG_CORPUS") else [],
    similarity_top_k=5,
)

rag_agent = Agent(
    name="RAGAgent",
    model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"),
    instruction="You are a specialist in retrieving college information. Given a college name, use the 'retrieve_rag_documentation' tool to find data like GPA, test scores, and acceptance rates. Your final output to the Coordinator MUST be a single, concise text string summarizing the findings or clearly stating if specific data was not found or if the retrieval failed. Example: 'For [College Name]: Avg GPA: 3.5, SAT Range: 1200-1400, Acceptance Rate: 15%. Median ACT not found.' OR 'For [College Name]: Failed to retrieve data.'",
    tools=[vertex_rag_retrieval_tool]
)

# 2. Search Agent
search_agent = Agent(
    name="SearchAgent",
    model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"),
    instruction="You are a specialist in web searches for recent information. Given a college name and a query about recent news/policies, use Google Search. Your final output to the Coordinator MUST be a single, concise text string summarizing relevant findings (e.g., specific policy changes, dates) or stating 'No relevant recent information found' or 'Search failed.' Example: 'For [College Name]: Found a policy update on their website dated YYYY-MM-DD regarding test-optional status.' OR 'For [College Name]: No major admission policy changes found in the last 3-6 months.'",
    tools=[google_search]
)

# 3. Coding Agent
coding_agent = Agent(
    name="CodingAgent",
    model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"),
    instruction="You are a specialist in executing Python code for calculations. Given a specific calculation request with all necessary inputs, write and execute the code. Your final output to the Coordinator MUST be a single text string with the numerical result or a clear error message. Example: 'Calculation result: 42.' OR 'Error: Division by zero.'",
    tools=[built_in_code_execution]
)

# --- Root Agent Definition ---

# Configure Automatic Function Calling for the Root Agent
# We estimate roughly 3 sub-agent calls per college (RAG, Search, Code).
# For up to 15-16 sub-agent calls, set maximum_remote_calls to ~50 for a good buffer.
coordinator_afc_settings = genai_types.AutomaticFunctionCallingConfig(
    maximum_remote_calls=50
)

# Create GenerateContentConfig for the coordinator agent
# This is where AFC settings are passed for an ADK Agent
coordinator_generate_content_config = genai_types.GenerateContentConfig(
    automatic_function_calling=coordinator_afc_settings
    # We could also include a tool_config here if needed for other AFC behaviors like mode='ANY'
    # For example: 
    # tool_config=genai_types.ToolConfig(
    #    function_calling_config=genai_types.FunctionCallingConfig(mode='ANY')
    # )
)

internal_coordinator_agent = Agent(
    name="InternalCoordinatorAgent",
    model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"),
    description="Coordinates multiple specialist agents to provide college admission chance analysis.",
    instruction=get_internal_coordinator_instructions(),
    tools=[
        AgentTool(agent=rag_agent),
        AgentTool(agent=search_agent),
        AgentTool(agent=coding_agent)
    ],
    # Pass the custom GenerateContentConfig here
    generate_content_config=coordinator_generate_content_config 
)

# --- Presenter Agent Definition ---
presenter_agent = Agent(
    name="PresenterAgent",
    model=os.getenv("ADK_MODEL_NAME", "gemini-2.5-flash-preview-04-17"),
    instruction=get_presenter_agent_instructions(),
    tools=[
        AgentTool(agent=internal_coordinator_agent)
    ]
    # No special generate_content_config likely needed, default AFC limit is fine for one call.
)

# The main agent exposed by this module is now the presenter
root_agent = presenter_agent

if __name__ == "__main__":
    # This section is for local testing if you run 'python insight_agent/agent.py'
    # However, ADK's primary way of running is via 'adk run' or 'adk web'.
    print("Project Insight Multi-Agent System Loaded.")
    print(f"Root Agent Name: {root_agent.name}")
    print(f"Root Agent Model: {root_agent.model}")
    print(f"Root Agent Tools (Sub-Agents): {[tool.agent.name for tool in root_agent.tools if isinstance(tool, AgentTool)]}")

    if not os.environ.get("RAG_CORPUS"):
        print("\nWARNING: RAG_CORPUS environment variable is not set. ")
        print("The 'RAGAgent' and its 'retrieve_rag_documentation' tool will not function without it.")
    elif not vertex_rag_retrieval_tool.rag_resources: # Check if it was set but list is empty
        print("\nWARNING: RAG_CORPUS was set, but RAG tool's rag_resources list is empty.")
        print("The 'RAGAgent' may not function correctly.")

    # Note: Direct interaction loop from original single-agent setup is removed
    # as 'adk run' or 'adk web' would be the primary way to interact with the root_agent.
    # The previous loop for direct 'python insight_agent/agent.py' interaction
    # would need significant changes to work with the async nature of multi-agent calls.
    print("\nTo interact with the agent, use 'adk run insight_agent.agent' or 'adk web insight_agent.agent'")

    # To interact directly here, you would need to set up a session and run loop,
    # which 'adk run' handles. For example:
    #
    # from google.adk.sessions import Session
    # async def main():
    #     async with Session() as session:
    #         print("Enter your query or type 'exit' to end.")
    #         while True:
    #             user_input = input("You: ")
    #             if user_input.lower() == 'exit':
    #                 break
    #             response = await root_agent.send(session_id=session.id, message=user_input)
    #             print(f"Agent: {response.text}")
    #
    # import asyncio
    # asyncio.run(main()) 