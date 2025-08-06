# Graphiti Knowledge Base - Key Insights

## 🏗️ Architecture & Design Patterns

### Core Architecture
- **Main Entry Point**: `graphiti_core/graphiti.py` - The central `Graphiti` class orchestrates all functionality
- **Bi-temporal Data Model**: Tracks both event occurrence time and knowledge ingestion time
- **Episode-based Ingestion**: Data added as "episodes" containing facts/triplets
- **Hybrid Search**: Combines semantic embeddings, BM25 keyword search, and graph traversal

### Design Patterns
- **Driver Pattern**: Abstract interface with Neo4j and FalkorDB implementations
- **Client Pattern**: Pluggable LLM, embedding, and cross-encoder providers
- **Pydantic Models**: Strong typing and validation throughout
- **Temporal Handling**: Uses `valid_from`/`invalid_from` for relationship changes

## 🚀 Key Features & Capabilities

### Core Features
- **Real-Time Incremental Updates**: No batch recomputation needed
- **Point-in-Time Queries**: Historical context with temporal awareness
- **Custom Entity Definitions**: Flexible ontology via Pydantic models
- **Multi-Database Support**: Neo4j (primary) and FalkorDB
- **Multi-LLM Support**: OpenAI, Anthropic, Gemini, Groq, Azure OpenAI, Ollama

### Search Capabilities
- **Search Methods**: Cosine similarity, BM25, breadth-first search
- **Rerankers**: RRF, node distance, episode mentions, MMR, cross-encoder
- **Search Recipes**: Pre-configured strategies for common patterns
- **Flexible Configuration**: Customizable per entity type

## 📖 API Usage Examples

### Basic Usage
```python
# Initialize
graphiti = Graphiti(uri, user, password)
await graphiti.build_indices_and_constraints()

# Add episodes
await graphiti.add_episode(
    name="Episode Name",
    episode_body="Content to process",
    source_description="Source info"
)

# Search
results = await graphiti.search(
    query="What is X?",
    search_config=EDGE_HYBRID_SEARCH_RRF
)
```

### Ollama Integration (OpenAI-Compatible)
```python
# Configuration
OPENAI_API_KEY=dummy-key-for-ollama
OPENAI_BASE_URL=http://localhost:11434/v1
MODEL_NAME=llama3.2
EMBEDDING_MODEL=nomic-embed-text
```

## ⚙️ Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-key

# Performance
SEMAPHORE_LIMIT=10  # LLM concurrency (increase for better performance)
USE_PARALLEL_RUNTIME=false  # Neo4j enterprise feature

# Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# Optional Providers
ANTHROPIC_API_KEY=optional
GOOGLE_API_KEY=optional
GROQ_API_KEY=optional
VOYAGE_API_KEY=optional
```

### Custom Database Configuration
```python
driver = Neo4jDriver(
    uri="bolt://localhost:7687",
    user="neo4j",
    password="password",
    database="custom_db"  # Override default 'neo4j'
)
graphiti = Graphiti(graph_driver=driver)
```

## 🎯 Best Practices

### Development Workflow
```bash
make install    # Install with uv
make format     # Format with ruff
make lint       # Lint and type check
make test       # Run tests
make check      # All checks
```

### Code Standards
- **Formatting**: Ruff, 100 char lines, single quotes
- **Type Checking**: Pyright (basic for core, standard for server)
- **Testing**: Unit tests + integration tests (marked with `_int`)
- **Imports**: TYPE_CHECKING pattern for optional dependencies

### Performance Optimization
1. **Provider Selection**: Use OpenAI/Gemini for structured output support
2. **Concurrency**: Increase `SEMAPHORE_LIMIT` for provider limits
3. **Database**: Use Neo4j Enterprise parallel runtime for scale
4. **Search Strategy**: Choose appropriate rerankers (cross-encoder for accuracy, RRF for speed)

## 🔌 Integration Patterns

### MCP Server (Model Context Protocol)
- **Location**: `mcp_server/`
- **Transport**: SSE for real-time communication
- **Deployment**: Docker Compose with Neo4j
- **Memory Pattern**: Preference/Procedure/Fact-based

### REST API Service
- **Location**: `server/`
- **Framework**: FastAPI
- **Deployment**: Docker Compose
- **Features**: Health checks, Swagger docs

### Key Integration Files
- **MCP Server**: `mcp_server/graphiti_mcp_server.py`
- **REST API**: `server/graph_service/main.py`
- **Examples**: `examples/quickstart/`, `examples/ecommerce/`

## 🧪 Testing Strategy

### Test Organization
- **Unit Tests**: No external dependencies
- **Integration Tests**: Database required (`*_int.py`)
- **Evaluation**: LongMemEval dataset benchmarking
- **Provider Tests**: Separate suites per LLM

### Running Tests
```bash
pytest                    # All tests
pytest -k "not _int"      # Unit tests only
pytest -k "_int"          # Integration tests only
pytest -n auto            # Parallel execution
```

## 📊 Performance Considerations

### Scaling Recommendations
- **High Throughput**: Increase `SEMAPHORE_LIMIT` (default: 10)
- **Large Datasets**: Use Neo4j Enterprise with parallel runtime
- **Production**: Consider AuraDB Enterprise
- **LLM Selection**: Prefer providers with structured output

### Query Optimization
- **Search Recipes**: Use predefined configurations
- **Reranker Selection**: Balance accuracy vs speed
- **Temporal Queries**: Leverage bi-temporal indexing

## 🗂️ Key Files Reference

1. **Core**: `graphiti_core/graphiti.py`
2. **Search**: `graphiti_core/search/search_config_recipes.py`
3. **LLM Clients**: `graphiti_core/llm_client/`
4. **Drivers**: `graphiti_core/driver/`
5. **Prompts**: `graphiti_core/prompts/`
6. **MCP**: `mcp_server/graphiti_mcp_server.py`
7. **API**: `server/graph_service/main.py`
8. **Config**: `pyproject.toml`
9. **Docs**: `README.md`, `CLAUDE.md`

## 🔧 Common Operations

### Adding a New LLM Provider
1. Create client in `graphiti_core/llm_client/`
2. Implement `LLMClient` interface
3. Add configuration in `llm_client/config.py`
4. Update documentation

### Adding a New Database Backend
1. Create driver in `graphiti_core/driver/`
2. Implement `DriverBase` interface
3. Add queries in `models/`
4. Update tests

### Debugging Tips
- Enable debug logging in application
- Use Neo4j Browser for visualization
- Run `pytest -s` for print statements
- Check database connection for integration test failures