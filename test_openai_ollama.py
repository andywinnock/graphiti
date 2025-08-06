#!/usr/bin/env python3
"""
Test script to verify Ollama works via OpenAI-compatible API
"""

import asyncio
import os
from datetime import datetime

from graphiti_core import Graphiti
from graphiti_core.llm_client import LLMConfig
from graphiti_core.llm_client.openai_client import OpenAIClient
from graphiti_core.embedder.openai import OpenAIEmbedder, OpenAIEmbedderConfig


async def test_openai_ollama():
    """Test Ollama via OpenAI-compatible API"""
    print("🧪 Testing Ollama via OpenAI-Compatible API")
    print("=" * 50)
    
    try:
        # Setup OpenAI client pointed at Ollama
        llm_config = LLMConfig(
            api_key='dummy-key-for-ollama',
            base_url='http://localhost:11434/v1',
            model='llama3.2',
            small_model='llama3.2',
        )
        
        openai_client = OpenAIClient(config=llm_config)
        print("✅ OpenAI client configured for Ollama")
        
        # Setup embedder using OpenAI client for Ollama
        embedder_config = OpenAIEmbedderConfig(
            api_key='dummy-key-for-ollama',
            base_url='http://localhost:11434/v1',
            embedding_model='nomic-embed-text'
        )
        
        openai_embedder = OpenAIEmbedder(config=embedder_config)
        print("✅ OpenAI embedder configured for Ollama")
        
        # Test basic LLM functionality
        print("\n🔍 Testing LLM functionality...")
        messages = [{"role": "user", "content": "Hello! Respond with just 'Hello from Ollama!'"}]
        
        response = await openai_client.client.chat.completions.create(
            model="llama3.2",
            messages=messages,
            temperature=0.0,
            max_tokens=50
        )
        
        llm_response = response.choices[0].message.content
        print(f"📝 LLM Response: {llm_response}")
        
        # Test embedding functionality
        print("\n🔍 Testing embedding functionality...")
        embedding = await openai_embedder.create("Test embedding text")
        print(f"📊 Embedding dimension: {len(embedding)}")
        
        # Test Graphiti initialization
        print("\n🔍 Testing Graphiti with OpenAI-Ollama setup...")
        graphiti = Graphiti(
            uri="bolt://localhost:7687",
            user="neo4j",
            password="demodemo",
            llm_client=openai_client,
            embedder=openai_embedder
        )
        
        print("✅ Graphiti initialized with OpenAI-Ollama clients")
        
        # Test entity extraction
        print("\n🔍 Testing entity extraction...")
        episode_result = await graphiti.add_episode(
            name="OpenAI-Ollama Test",
            episode_body="Tesla is an electric vehicle company founded by Elon Musk. They manufacture cars like Model 3 and Model Y.",
            source_description="OpenAI-compatible API test",
            reference_time=datetime.now()
        )
        
        print("✅ Entity extraction completed successfully!")
        print("🎯 OpenAI-compatible Ollama integration is working!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_openai_ollama())