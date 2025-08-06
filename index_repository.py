#!/usr/bin/env python3
"""
Index Graphiti repository insights into the knowledge graph
"""

import asyncio
import os
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig


async def index_graphiti_repository():
    """Index key Graphiti insights into the knowledge graph"""
    print("🚀 Indexing Graphiti Repository Insights")
    print("=" * 50)
    
    # Setup OpenAI client for Ollama
    llm_config = LLMConfig(
        api_key='dummy-key-for-ollama',
        base_url='http://localhost:11434/v1',
        model='llama3.2',
        small_model='llama3.2',
    )
    
    # Setup embedder
    embedder_config = OpenAIEmbedderConfig(
        api_key='dummy-key-for-ollama',
        base_url='http://localhost:11434/v1',
        embedding_model='nomic-embed-text'
    )
    
    # Initialize Graphiti
    graphiti = Graphiti(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="demodemo",
        llm_client=OpenAIClient(config=llm_config),
        embedder=OpenAIEmbedder(config=embedder_config)
    )
    
    print("✅ Graphiti initialized with Ollama")
    
    # Define episodes to add
    episodes = [
        {
            "name": "Graphiti Architecture Overview",
            "body": """
            Graphiti is a Python framework for building temporally-aware knowledge graphs for AI agents.
            The main entry point is the Graphiti class in graphiti_core/graphiti.py.
            It uses a bi-temporal data model tracking both event occurrence and ingestion times.
            The architecture follows modular design with driver pattern for databases (Neo4j, FalkorDB),
            client pattern for LLM providers (OpenAI, Anthropic, Gemini, Groq, Ollama),
            and episode-based ingestion where data is added as episodes containing facts.
            """,
            "description": "Core architecture and design patterns"
        },
        {
            "name": "Graphiti Search Capabilities",
            "body": """
            Graphiti provides hybrid search combining semantic embeddings, BM25 keyword search, 
            and graph traversal. Search methods include cosine similarity, BM25, and breadth-first search.
            Multiple rerankers are available: RRF (reciprocal rank fusion), node distance, 
            episode mentions, MMR (maximal marginal relevance), and cross-encoder.
            Pre-configured search recipes are provided for common patterns.
            """,
            "description": "Search features and capabilities"
        },
        {
            "name": "Graphiti Configuration and Setup",
            "body": """
            Graphiti requires OPENAI_API_KEY environment variable. For Ollama integration,
            set OPENAI_BASE_URL to http://localhost:11434/v1 with dummy API key.
            Performance tuning includes SEMAPHORE_LIMIT (default 10) for LLM concurrency.
            Database configuration supports custom Neo4j database names via driver parameter.
            Multiple LLM providers supported: OpenAI, Anthropic, Gemini, Groq, Azure OpenAI, Ollama.
            """,
            "description": "Configuration and environment setup"
        },
        {
            "name": "Graphiti Development Workflow",
            "body": """
            Development uses uv for dependency management with commands: make install, make format,
            make lint, make test, make check. Code standards include Ruff formatting with 100 char lines,
            single quotes, and Pyright type checking. Testing separates unit tests from integration tests
            marked with _int suffix. Use pytest -n auto for parallel test execution.
            """,
            "description": "Development practices and workflow"
        },
        {
            "name": "Graphiti MCP Server Integration",
            "body": """
            The MCP (Model Context Protocol) server in mcp_server/ provides AI assistant integration.
            It supports SSE transport for real-time communication, Docker deployment with Neo4j,
            and memory patterns based on preferences, procedures, and facts.
            Configuration via docker-compose.yml with environment variables for Ollama integration.
            """,
            "description": "MCP server for AI assistants"
        },
        {
            "name": "Graphiti Performance Optimization",
            "body": """
            Performance optimization strategies include: increasing SEMAPHORE_LIMIT for higher throughput,
            using Neo4j Enterprise parallel runtime for large datasets, selecting LLM providers with
            structured output support (OpenAI, Gemini), choosing appropriate search rerankers
            (cross-encoder for accuracy, RRF for speed), and leveraging bi-temporal indexing for queries.
            """,
            "description": "Performance tuning and optimization"
        }
    ]
    
    # Add episodes to the graph
    for i, episode in enumerate(episodes, 1):
        print(f"\n📝 Adding episode {i}/{len(episodes)}: {episode['name']}")
        try:
            await graphiti.add_episode(
                name=episode["name"],
                episode_body=episode["body"],
                source_description=episode["description"],
                reference_time=datetime.now()
            )
            print(f"   ✅ Successfully indexed")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n🔍 Testing search functionality...")
    
    # Test searches
    test_queries = [
        "How does Graphiti handle search?",
        "What LLM providers are supported?",
        "How to configure Ollama?",
        "What are the development commands?"
    ]
    
    for query in test_queries:
        print(f"\n💭 Query: {query}")
        try:
            results = await graphiti.search(query, num_results=3)
            if results:
                print(f"   Found {len(results)} results")
                for j, result in enumerate(results[:2], 1):
                    result_type = type(result).__name__
                    result_name = getattr(result, 'name', getattr(result, 'fact', 'Unknown'))
                    print(f"   {j}. {result_type}: {result_name[:60]}...")
            else:
                print("   No results found")
        except Exception as e:
            print(f"   ❌ Search error: {e}")
    
    print("\n✅ Repository indexing complete!")
    print("📊 Knowledge graph now contains Graphiti insights")


if __name__ == "__main__":
    asyncio.run(index_graphiti_repository())