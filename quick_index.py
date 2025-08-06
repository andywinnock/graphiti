#!/usr/bin/env python3
"""
Quick index of Graphiti repository insights
"""

import asyncio
from datetime import datetime
from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig


async def quick_index():
    """Quick index of key Graphiti facts"""
    print("🚀 Quick Indexing Graphiti Facts")
    print("=" * 40)
    
    # Setup
    llm_config = LLMConfig(
        api_key='dummy-key-for-ollama',
        base_url='http://localhost:11434/v1',
        model='llama3.2',
        small_model='llama3.2',
    )
    
    embedder_config = OpenAIEmbedderConfig(
        api_key='dummy-key-for-ollama',
        base_url='http://localhost:11434/v1',
        embedding_model='nomic-embed-text'
    )
    
    graphiti = Graphiti(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="demodemo",
        llm_client=OpenAIClient(config=llm_config),
        embedder=OpenAIEmbedder(config=embedder_config)
    )
    
    # Add one comprehensive episode
    episode = """
    Graphiti is a Python framework for temporally-aware knowledge graphs. 
    Main features: bi-temporal data model, episode-based ingestion, hybrid search.
    Supports Neo4j and FalkorDB. LLM providers: OpenAI, Anthropic, Gemini, Groq, Ollama.
    For Ollama: set OPENAI_BASE_URL=http://localhost:11434/v1 with dummy API key.
    Key files: graphiti_core/graphiti.py (main class), mcp_server/ (AI assistant integration).
    Search methods: cosine similarity, BM25, graph traversal. Rerankers: RRF, cross-encoder.
    Development: make install, make format, make lint, make test. Uses uv, ruff, pyright.
    Performance: increase SEMAPHORE_LIMIT for concurrency, use structured output LLMs.
    """
    
    print("📝 Adding Graphiti overview...")
    await graphiti.add_episode(
        name="Graphiti Framework Overview",
        episode_body=episode,
        source_description="Repository documentation summary",
        reference_time=datetime.now()
    )
    
    print("✅ Indexing complete!")
    
    # Quick search test
    print("\n🔍 Testing search...")
    results = await graphiti.search("How to use Ollama with Graphiti?", num_results=3)
    print(f"Found {len(results)} results")
    
    return True


if __name__ == "__main__":
    asyncio.run(quick_index())