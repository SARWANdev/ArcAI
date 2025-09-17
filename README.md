# ArcAI - AI-Powered Academic PDF Library

ArcAI is an intelligent document management system designed to help university students, researchers, HiWi workers, and doctoral candidates effectively manage, understand, and interact with academic papers. The platform combines document organization with AI-powered assistance to simplify academic research workflows.

## Vision

ArcAI makes academic reading, understanding, and organization simpler by providing:
- **Structured Workspace**: Import and organize papers in a systematic manner
- **Intelligent Highlighting**: Mark important passages and take contextual notes
- **AI Assistant**: Built-in paper-aware AI for summarization, explanation, and clarification
- **Unified Platform**: No need to switch between separate tools or generic chatbots

## Target Audience

- University students and researchers
- HiWi assistants and doctoral candidates
- Professors and academic staff
- Anyone working with academic literature who needs assistance understanding complex concepts

## System Architecture

ArcAI implements a **RAG (Retrieval-Augmented Generation) pipeline** that enables users to query their PDF collection and receive contextually grounded answers. The development consistently applied the MVCS structure, along with the exceptions and
repository layers. The view is implemented using React, which made it possible to develop the
frontend separately from the backend. It communicates with the backend through controller
classes, which were kept minimal and free of business logic to keep the interface clean and
focused.

### Backend Technology Stack
- **Framework**: Flask (Python) with REST API
- **PDF Processing**: PyPDF2 for text extraction
- **AI/ML**: 
  - Embeddings: Nomic Embed Text via OLLAMA API
  - Language Model: Gemma V3 via OLLAMA API
  - Vector Search: FAISS (Facebook AI Similarity Search)
- **Databases**:
  - MongoDB: Document metadata and embeddings storage
  - Elasticsearch: Fast full-text search across PDFs
- **Authentication**: OAuth integration
- **File Storage**: Remote server with SSH/SCP

### Frontend Technology Stack
- **Framework**: React with Vite
- **UI Components**: Bootstrap 5 with React Bootstrap
- **HTTP Client**: Axios
- **Styling**: Styled Components

## Project Structure

```
arcai/
├── main.py                          # Flask application entry point
├── requirements.txt                 # Python dependencies
├── package.json                     # Frontend dependencies
├── controller/                      # API controllers
│   ├── chat_controller.py          # AI chat endpoints
│   ├── document_controller.py      # Document management
│   ├── project_controller.py       # Project organization
│   ├── library_controller.py       # Library management
│   └── user_controller.py          # User authentication
├── model/                          # Data models
│   ├── ai_chat/
│   │   └── conversation.py         # Conversation model
│   ├── document_reader/
│   │   ├── document.py            # Document model
│   │   ├── project.py             # Project model
│   │   ├── pdf_master.py          # PDF master model
│   │   └── tag_manager/           # Tag system
│   └── user_profile/
│       └── user.py                # User model
├── services/                       # Business logic
│   ├── ai_service.py              # AI/LLM integration
│   ├── document_manager/          # Document processing
│   ├── upload_manager/            # File upload & embeddings
│   ├── user_management/           # Authentication & users
│   ├── bibtex_service.py         # Bibliography management
│   ├── conversation_service.py   # Chat management
│   └── notebook_service.py       # Note-taking
├── database/                       # Data persistence
│   ├── repository/                # Data access layer
│   └── utils/                     # Database utilities
├── exceptions/                     # Custom exception handling
└── tests/                         # Comprehensive test suite
```

##  Key Features

### Document Management
- **Upload & Deduplication**: Hash-based file deduplication prevents duplicate uploads
- **PDF Processing**: Automatic text extraction and metadata parsing
- **Vector Embeddings**: FAISS-based semantic search capabilities
- **Tag System**: Color-coded tagging for organization
- **Status Tracking**: Read/unread and favorite markers

### AI-Powered Assistance
- **Contextual Chat**: AI assistant with access to your document library
- **RAG Pipeline**: Retrieval-augmented generation for accurate responses
- **Multi-Document Queries**: Query across multiple papers simultaneously
- **Conversation Management**: Persistent chat history with automatic naming

### Organization & Search
- **Project-Based Organization**: Group documents by research topics
- **Full-Text Search**: Elasticsearch-powered content search
- **Semantic Search**: Vector similarity search for concept-based queries
- **Filtering & Sorting**: By read status, favorites, tags, and metadata

### Bibliography Management
- **BibTeX Integration**: Automatic citation extraction and formatting
- **Metadata Extraction**: Author, year, source, and publication details
- **Citation Support**: Habanero integration for DOI-based metadata

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB
- Elasticsearch
- OLLAMA (for AI models)

### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd arcai
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration**:
   Create a `.env` file with the following variables:
   ```env
   # Database Configuration
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=arcai1
   ELASTIC_URI=https://127.0.0.1:9200
   ELASTIC_USER=elastic
   ELASTIC_PASSWORD=your_password

   # AI Model Configuration
   OLLAMA_DEFAULT_BASE_URL=http://127.0.0.1:11435
   OLLAMA_DEFAULT_EMBEDDING_MODEL=nomic-embed-text
   OLLAMA_DEFAULT_LLM=gemma3

   # Application Configuration
   APP_SECRET_KEY=your_secret_key
   FRONTEND_URL=http://localhost:5173
   PORT=3000
   ```

4. **Start the Flask server**:
   ```bash
   python main.py
   ```

### Frontend Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Start the development server**:
   ```bash
   npm run dev
   ```

## Configuration

### AI Models
The system supports swappable AI models (configurable by administrators):
- **Embedding Model**: Nomic Embed Text (default)
- **Language Model**: Gemma V3 (default)
- **Base URL**: Configurable OLLAMA endpoint

### Database Setup
- **MongoDB**: Stores user data, documents, projects, and conversations
- **Elasticsearch**: Indexes PDF content for full-text search
- **FAISS**: Vector storage for semantic search

## API Endpoints

### Document Management
- `POST /document/upload` - Upload PDF documents
- `GET /document/{id}` - Retrieve document details
- `DELETE /document/{id}` - Delete document
- `PUT /document/tag` - Add/update document tags
- `GET /document/download/{id}` - Download PDF file

### Project Organization
- `GET /project/{id}/documents` - Get project documents
- `PUT /project/document/rename` - Rename documents
- `POST /project/document/move` - Move documents between projects

### AI Chat
- `POST /chat/query` - Send query to AI assistant
- `GET /chat/conversations` - Get conversation history
- `POST /chat/conversation/rename` - Rename conversations
- `DELETE /chat/conversation/{id}` - Delete conversation

### User Management
- OAuth-based authentication
- User profile management
- Library and project access control

## Testing

The project includes comprehensive test coverage:
- Repository layer tests
- Service layer tests
- API endpoint tests
- Integration tests

Run tests with:
```bash
pytest
```

## Security Features

- OAuth authentication
- User-scoped data access
- File validation and size limits
- Secure file storage
- Input sanitization

## Deployment

The application is designed for deployment with:
- Environment-based configuration
- Docker support (configurable)
- Remote file storage capabilities
- Scalable database architecture

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For support and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information


## Deployment

The application is designed for deployment with:
- Environment-based configuration
- Docker support (configurable)
- Remote file storage capabilities
- Scalable database architecture

### Deployment Guide

To start the ArcAI system and all required services, follow the steps below:

1. **Access the Server**  
   Log in to the server via SSH using your assigned credentials:  

    ```bash
    ssh pse04@i83compute4.dcn.itec.kit.edu
    ```

2. **Navigate to the Project Directory**  

    ```bash
    cd pse04/arcai
    ```

3. **Run the Deployment Script**  
   Execute the provided startup script to launch all components of the system (frontend, backend, database, and AI services):  

    ```bash
    ./everything.sh
    ```

   The script starts all services and keeps them running in the background until explicitly terminated.

---

### Accessing the Application Externally

If you wish to access the application from outside the server, create SSH tunnels from your local machine to the server as follows:

```bash
ssh -L 5173:localhost:5173 pse04@i83compute4.dcn.itec.kit.edu
ssh -L 3000:localhost:3000 pse04@i83compute4.dcn.itec.kit.edu
```


After setting up the tunnels, the application will be accessible in your local browser at:

http://localhost:5173

---

**ArcAI** - Making academic research more accessible through intelligent document management and AI assistance.