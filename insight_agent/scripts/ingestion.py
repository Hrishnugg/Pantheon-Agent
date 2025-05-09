# insight_agent/scripts/ingestion.py

import os
import sys
from dotenv import load_dotenv

# Ensure the insight_agent package root is in the Python path
# This allows a_i_m_l_path_to_insert_sys_path_statement_for_insight_agent

try:
    import vertexai
    from vertexai import rag # For RAG specific operations
    from google.auth import default as google_auth_default # To get credentials for init
    from google.api_core import exceptions as google_exceptions 
except ImportError as e:
    print(f"Google Cloud SDK or auth library not found: {e}. Please ensure it's installed.")
    print("You might need to run: pip install google-cloud-aiplatform[rag] vertexai google-auth --upgrade")
    sys.exit(1)

# --- Configuration ---
# Construct the path to the .env file located in the insight_agent directory
# This script is in insight_agent/scripts/, so .env is one level up.
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")
# RAG_CORPUS_ENV_VAR should be the full resource name from .env if already created
# e.g., projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{CORPUS_ID}
RAG_CORPUS_ENV_VAR = os.getenv("RAG_CORPUS")

# Optional: If you want the script to create the corpus if it doesn't exist
# and RAG_CORPUS is not set in .env
CORPUS_DEFAULT_DISPLAY_NAME = "Project Insight College Data Corpus"
CORPUS_DEFAULT_DESCRIPTION = "Corpus containing data about US colleges for Project Insight RAG."

# --- Helper Functions --- 

def init_vertex_ai():
    """Initializes Vertex AI SDK with project, location, and credentials."""
    if not PROJECT_ID or not LOCATION:
        print("Error: GOOGLE_CLOUD_PROJECT or GOOGLE_CLOUD_LOCATION not set in .env")
        sys.exit(1)
    try:
        credentials, project_from_adc = google_auth_default()
        vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials)
        print(f"Vertex AI SDK initialized for project: {PROJECT_ID} in location: {LOCATION}")
    except Exception as e:
        print(f"Error initializing Vertex AI SDK: {e}")
        print("Ensure GOOGLE_APPLICATION_CREDENTIALS is set correctly if using a service account, or run `gcloud auth application-default login`.")
        sys.exit(1)

def create_or_get_rag_corpus(display_name_if_creating, description_if_creating):
    """Uses RAG_CORPUS from .env if set, otherwise tries to create or find an existing one."""
    if RAG_CORPUS_ENV_VAR:
        print(f"Using RAG_CORPUS from environment: {RAG_CORPUS_ENV_VAR}")
        try:
            # Verify by trying to get it (rag.get_corpus is not directly available, have to list and match by name)
            # Or assume if it's in .env, it's valid until an operation fails.
            # For simplicity, we'll proceed if it's set. Operations will fail if it's invalid.
            print(f"Proceeding with corpus: {RAG_CORPUS_ENV_VAR}")
            return RAG_CORPUS_ENV_VAR # Return the full resource name
        except Exception as e:
            # This block might not be reachable if we just return above, 
            # but kept for conceptual completeness if a get_corpus existed.
            print(f"Error with provided RAG_CORPUS '{RAG_CORPUS_ENV_VAR}': {e}. Please check.")
            return None

    print(f"RAG_CORPUS not set in .env. Attempting to find or create corpus with display name: '{display_name_if_creating}'...")
    try:
        existing_corpora = rag.list_corpora()
        for corpus_obj in existing_corpora:
            if corpus_obj.display_name == display_name_if_creating:
                print(f"Found existing corpus: {corpus_obj.display_name} (Name: {corpus_obj.name})")
                print(f"IMPORTANT: Consider setting RAG_CORPUS={corpus_obj.name} in your .env file.")
                return corpus_obj.name # Return the full resource name
    except Exception as e:
        print(f"Error listing existing corpora: {e}. Will attempt to create a new one.")

    print(f"Creating new RAG Corpus with display name: {display_name_if_creating}")
    try:
        # Embedding model config might be needed for create_corpus
        # Example from adk-samples: publishers/google/models/text-embedding-004
        # Check vertexai.rag.EmbeddingModelConfig documentation for latest way to specify
        new_corpus = rag.create_corpus(
            display_name=display_name_if_creating,
            description=description_if_creating
            # embedding_model_config might be required by the SDK or have defaults
        )
        print(f"Created RAG Corpus: {new_corpus.name} (Display: {new_corpus.display_name})")
        print(f"IMPORTANT: Update your .env file with: RAG_CORPUS={new_corpus.name}")
        return new_corpus.name # Return the full resource name
    except Exception as e:
        import traceback
        print(f"Error creating RAG Corpus: {e}")
        traceback.print_exc()
        print("Please ensure Vertex AI RAG Engine API is enabled and you have permissions.")
        return None

def upload_file_to_rag_corpus(corpus_resource_name, file_path, display_name_for_file):
    """Uploads a single file to the specified RAG corpus using vertexai.rag.upload_file."""
    print(f"Attempting to upload '{file_path}' to corpus '{corpus_resource_name}' as '{display_name_for_file}'...")
    try:
        # vertexai.rag.upload_file is a higher-level API.
        # Ensure vertexai.init() has been called.
        upload_response = rag.upload_file(
            corpus_name=corpus_resource_name, # This should be the full resource name
            path=file_path,
            display_name=display_name_for_file,
            description=f"Uploaded file {display_name_for_file}" 
        )
        print(f"Successfully initiated upload for '{display_name_for_file}'. Response: {upload_response}")
        return True
    except Exception as e:
        import traceback
        print(f"Error uploading file '{file_path}' using vertexai.rag.upload_file: {e}")
        traceback.print_exc()
        print("Ensure the RAG corpus exists, path is correct, and you have permissions.")
        return False

def list_files_in_rag_corpus(corpus_resource_name):
    """Lists files in the specified RAG corpus using vertexai.rag.list_files."""
    print(f"\nFiles in RAG Corpus '{corpus_resource_name}':")
    try:
        rag_files = rag.list_files(corpus_name=corpus_resource_name)
        if not rag_files:
            print("  No files found.")
            return
        for rag_file in rag_files:
            # Accessing attributes might differ slightly depending on the RagFile object structure from vertexai.rag
            file_size = rag_file.size_bytes if hasattr(rag_file, 'size_bytes') else 'N/A'
            print(f"  - Display: {rag_file.display_name} (Name: {rag_file.name}, Size: {file_size} bytes)")
    except Exception as e:
        import traceback
        print(f"  Error listing files: {e}")
        traceback.print_exc()

# --- Main Ingestion Logic ---
def main():
    """Main function to run the ingestion process."""
    print("Starting RAG data ingestion process...")
    init_vertex_ai()

    target_corpus_name = create_or_get_rag_corpus(
        CORPUS_DEFAULT_DISPLAY_NAME, 
        CORPUS_DEFAULT_DESCRIPTION
    )
    
    if not target_corpus_name:
        print("Could not obtain a valid RAG corpus. Exiting ingestion.")
        return

    project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_dir = os.path.join(project_root_dir, 'data')
    
    sample_files_to_upload = []
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"Created dummy data directory: {data_dir}")
        except OSError as e:
            print(f"Error creating data directory {data_dir}: {e}. Please create it manually.")
            return

    dummy_files_info = [
        {"filename": "sample_cds_data_1.txt", "content": "College Name: Example University\nCommon Data Set 2023-2024\nSection C: First-Time, First-Year (Freshman) Admission\nC1. Applications: 10,000\nC2. Admitted: 2,500\nC7. SAT Evidence-Based Reading and Writing: 25th percentile 600, 75th percentile 700\nC7. SAT Math: 25th percentile 620, 75th percentile 730"},
        {"filename": "sample_ipeds_data_1.txt", "content": "IPEDS Data for Example College\nGraduation Rate (4-year): 60%\nStudent-to-Faculty Ratio: 15:1\nMost Popular Majors: Business, Psychology, Biology"},
        {"filename": "sample_college_website_snippet.txt", "content": "Welcome to Example College! We offer a vibrant campus life and world-class research opportunities in Computer Science. Our new AI lab opened last fall."}
    ]

    for info in dummy_files_info:
        file_path = os.path.join(data_dir, info["filename"])
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w", encoding='utf-8') as f:
                    f.write(info["content"])
                print(f"Created dummy file: {file_path}")
            except IOError as e:
                print(f"Error creating dummy file {file_path}: {e}")
        sample_files_to_upload.append({"path": file_path, "display_name": info["filename"]})

    if not sample_files_to_upload:
        print("No sample files configured or found to upload.")
        return # Exit if no files to upload

    successful_uploads = 0
    for file_info in sample_files_to_upload:
        if os.path.exists(file_info["path"]):
            if upload_file_to_rag_corpus(
                target_corpus_name, # Pass the full resource name
                file_info["path"],
                file_info["display_name"]
            ):
                successful_uploads += 1
        else:
            print(f"File not found, skipping: {file_info['path']}")
            
    print(f"\n{successful_uploads} out of {len(sample_files_to_upload)} files processed for upload.")
    
    list_files_in_rag_corpus(target_corpus_name) # Pass the full resource name
    print("\nIngestion process finished.")

if __name__ == "__main__":
    print("----------------------------------------------------------------------")
    print("IMPORTANT: Before running this script:")
    print("1. Ensure GOOGLE_APPLICATION_CREDENTIALS is set to a valid service account key JSON file if not using `gcloud auth application-default login`.")
    print("   Alternatively, ensure `gcloud auth application-default login` has been run recently.")
    print("2. Ensure GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION are set in insight_agent/.env")
    print("3. If you have an existing RAG Corpus, set RAG_CORPUS (full resource name) in .env.")
    print("   Otherwise, the script will attempt to create a new one.")
    print("4. The script will try to use/create a 'data' directory at the project root for sample files.")
    print("----------------------------------------------------------------------\n")
    main() 