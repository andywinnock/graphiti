#!/usr/bin/env python3
"""
Check what's in the Neo4j database
"""

from neo4j import GraphDatabase


def check_database():
    """Check Neo4j database contents"""
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "demodemo"))
    
    with driver.session() as session:
        # Count nodes
        result = session.run("MATCH (n) RETURN labels(n) as labels, count(n) as count")
        print("🗂️  Node counts by label:")
        for record in result:
            print(f"   {record['labels']}: {record['count']}")
        
        # Count relationships
        result = session.run("MATCH ()-[r]->() RETURN type(r) as type, count(r) as count")
        print("\n🔗 Relationship counts by type:")
        for record in result:
            print(f"   {record['type']}: {record['count']}")
        
        # Sample entities
        result = session.run("MATCH (n:Entity) RETURN n.name as name LIMIT 5")
        print("\n📝 Sample entities:")
        for record in result:
            print(f"   - {record['name']}")
        
        # Sample episodes
        result = session.run("MATCH (e:Episodic) RETURN e.name as name, e.created_at as created LIMIT 5")
        print("\n📖 Sample episodes:")
        for record in result:
            print(f"   - {record['name']} (created: {record['created']})")
    
    driver.close()
    print("\n✅ Database check complete")


if __name__ == "__main__":
    check_database()