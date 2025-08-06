# Complete Graphiti MCP Server Setup Guide

## 🎯 Purpose
This guide provides fail-proof instructions to set up the Graphiti MCP server on any new system, particularly optimized for work laptops with Docker and Ollama support.

## 📋 Prerequisites

### Required Software
1. **Git** - For cloning the repository
2. **Docker & Docker Compose** - For running Neo4j and the MCP server
3. **Python 3.10+** - For running the MCP server natively
4. **uv** - Python package manager (required for MCP)
5. **Ollama** (optional) - For local LLM support

### Required Accounts/Keys
- **OpenAI API Key** - OR Ollama installed locally
- **GitHub account** - For cloning your fork

## 🚀 Quick Start (Docker Method - Recommended)

### Step 1: Clone Your Fork
```bash
git clone https://github.com/andywinnock/graphiti.git
cd graphiti
```

### Step 2: Configure Environment
```bash
cd mcp_server

# Create .env file from example
cp .env.example .env

# Edit .env with your configuration
# For OpenAI:
echo "OPENAI_API_KEY=your-openai-key-here" >> .env
echo "MODEL_NAME=gpt-4o-mini" >> .env

# For Ollama (local LLM):
echo "OPENAI_API_KEY=dummy-key-for-ollama" >> .env
echo "OPENAI_BASE_URL=http://host.docker.internal:11434/v1" >> .env
echo "MODEL_NAME=llama3.2" >> .env
echo "SMALL_MODEL_NAME=llama3.2" >> .env
echo "EMBEDDING_MODEL=nomic-embed-text" >> .env
```

### Step 3: Start Services
```bash
# Start Neo4j and MCP server
docker compose up -d

# Verify services are running
docker compose ps

# Check logs
docker compose logs -f
```

### Step 4: Configure Your MCP Client (Claude/Cursor)

#### For Cursor (SSE Transport):
Add to Cursor's MCP configuration:
```json
{
  "mcpServers": {
    "graphiti-memory": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

#### For Claude Desktop (STDIO Transport):
Add to Claude's configuration (~/.config/claude/claude_desktop_config.json):
```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "/path/to/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/path/to/graphiti/mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "demodemo",
        "OPENAI_API_KEY": "your-key-here",
        "MODEL_NAME": "gpt-4o-mini"
      }
    }
  }
}
```

## 💻 Native Installation Method (Alternative)

### Step 1: Install uv
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Step 2: Install Neo4j
#### Option A: Docker
```bash
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/demodemo \
  neo4j:5.26.0
```

#### Option B: Neo4j Desktop
Download from: https://neo4j.com/download/

### Step 3: Setup Python Environment
```bash
cd graphiti/mcp_server

# Install dependencies
uv sync

# Verify installation
uv run python -c "import graphiti_core; print('✅ Graphiti installed')"
```

### Step 4: Run MCP Server
```bash
# For SSE transport (Cursor)
uv run graphiti_mcp_server.py --transport sse

# For STDIO transport (Claude Desktop)
uv run graphiti_mcp_server.py --transport stdio
```

## 🔧 Configuration Options

### Environment Variables
Create a `.env` file in the `mcp_server` directory:

```bash
# Core Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=demodemo

# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key
MODEL_NAME=gpt-4o-mini
SMALL_MODEL_NAME=gpt-4o-mini
LLM_TEMPERATURE=0.0

# Ollama Configuration (Alternative to OpenAI)
# OPENAI_API_KEY=dummy-key-for-ollama
# OPENAI_BASE_URL=http://localhost:11434/v1
# MODEL_NAME=llama3.2
# SMALL_MODEL_NAME=llama3.2
# EMBEDDING_MODEL=nomic-embed-text

# Performance
SEMAPHORE_LIMIT=10

# Telemetry (optional)
GRAPHITI_TELEMETRY_ENABLED=false
```

### Command Line Arguments
```bash
# Specify model
uv run graphiti_mcp_server.py --model gpt-4o-mini

# Set group ID for data namespace
uv run graphiti_mcp_server.py --group-id my-project

# Enable custom entity types
uv run graphiti_mcp_server.py --use-custom-entities

# Destroy existing graph on startup
uv run graphiti_mcp_server.py --destroy-graph
```

## 🧪 Testing the Setup

### Test 1: Verify Neo4j Connection
```bash
# Run the database check script
cd graphiti
python check_db.py
```

### Test 2: Test MCP Server
```python
# In your MCP client (Claude/Cursor), run:
await add_memory(
    name="Test Episode",
    episode_body={"test": "data", "working": true},
    source_description="Setup verification test"
)
```

### Test 3: Search Test
```python
# Search for the test data
results = await search_memory_facts("test data")
print(results)
```

## 🐳 Docker Compose Details

The `docker-compose.yml` includes:

```yaml
services:
  neo4j:
    image: neo4j:5.26.0
    ports:
      - "7474:7474"  # Web interface
      - "7687:7687"  # Bolt protocol
    environment:
      - NEO4J_AUTH=neo4j/demodemo
    healthcheck:
      test: ["CMD", "wget", "-O", "/dev/null", "http://localhost:7474"]

  graphiti-mcp:
    image: zepai/knowledge-graph-mcp:latest
    ports:
      - "8000:8000"  # SSE endpoint
    depends_on:
      neo4j:
        condition: service_healthy
    environment:
      - NEO4J_URI=bolt://neo4j:7687
      # All other env vars from .env file
```

## 🔍 Troubleshooting

### Issue: "Graphiti client not initialized"
**Solution:** Ensure Neo4j is running and accessible:
```bash
docker compose ps
docker compose restart neo4j
```

### Issue: "Connection refused on port 7687"
**Solution:** Check Neo4j is running:
```bash
# Docker method
docker logs neo4j

# Or check with curl
curl http://localhost:7474
```

### Issue: "Module not found" errors
**Solution:** Reinstall dependencies:
```bash
cd mcp_server
uv sync --refresh
```

### Issue: Rate limit errors (429)
**Solution:** Reduce concurrency:
```bash
export SEMAPHORE_LIMIT=5
```

### Issue: Ollama not working
**Solution:** Ensure Ollama is running:
```bash
# Start Ollama
ollama serve

# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text

# Test Ollama
curl http://localhost:11434/api/tags
```

## 📂 Important Files

### Configuration Files
- `mcp_server/.env` - Environment configuration
- `mcp_server/docker-compose.yml` - Docker services
- `mcp_server/pyproject.toml` - Python dependencies

### Modified Files (with enhancements)
- `mcp_server/graphiti_mcp_server.py` - Enhanced with automatic JSON handling

### Utility Scripts
- `check_db.py` - Verify Neo4j database contents
- `test_openai_ollama.py` - Test Ollama integration
- `index_repository.py` - Index Graphiti knowledge
- `quick_index.py` - Quick knowledge indexing

### Documentation
- `GRAPHITI_INSIGHTS.md` - Key insights and patterns
- `MCP_SETUP_GUIDE.md` - This setup guide

## 🚦 Quick Verification Checklist

- [ ] Neo4j accessible at http://localhost:7474
- [ ] MCP server running (check logs)
- [ ] Environment variables configured
- [ ] MCP client configured (Claude/Cursor)
- [ ] Test episode added successfully
- [ ] Search returns results

## 🆘 Support Resources

1. **Graphiti Documentation**: https://help.getzep.com/graphiti
2. **GitHub Issues**: https://github.com/getzep/graphiti/issues
3. **Discord**: https://discord.com/invite/W8Kw6bsgXQ
4. **MCP Documentation**: mcp_server/README.md

## 💡 Pro Tips

1. **For Work Laptops**: Use Docker method to avoid dependency conflicts
2. **For Local LLMs**: Ollama provides privacy and no API costs
3. **For Production**: Use OpenAI for better structured output support
4. **Performance**: Increase SEMAPHORE_LIMIT if your LLM provider allows
5. **Debugging**: Enable debug logging in graphiti_mcp_server.py

## 📝 Recent Enhancements

### Automatic JSON Handling (Latest)
The MCP server now automatically handles Python dictionaries and lists:
- No more manual JSON escaping required
- Automatic source detection for JSON data
- Full backward compatibility

Example:
```python
# Old way (manual escaping)
episode_body="{\"key\": \"value\"}"

# New way (automatic)
episode_body={"key": "value"}
```

---

**Last Updated**: December 2024
**Version**: Enhanced with automatic JSON handling
**Tested On**: macOS, Linux, Windows with Docker