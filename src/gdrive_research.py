from mcp.server import Server
from mcp.types import Resource
import asyncio
import json
import subprocess
import os

class GDriveResearch:
    def __init__(self):
        self.server = None
        
    async def start_server(self):
        """Start the MCP Google Drive server"""
        # Start the server process
        process = subprocess.Popen(
            ["npx", "-y", "@modelcontextprotocol/server-gdrive"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
        
    async def search_document(self, query: str):
        """Search for documents in Google Drive."""
        process = None
        try:
            process = await self.start_server()
            # Initialize server connection
            server = Server("gdrive-client")
            
            # Call the search tool
            results = await server.call_tool({
                "name": "search",
                "arguments": {"query": query}
            })
            if process:
                process.terminate()
            return results
            
        except Exception as e:
            print(f"Error during search: {e}")
            if process:
                process.terminate()
            return []
        
    async def read_document(self, file_id: str):
        """Read the contents of a specific Google Doc."""
        process = None
        try:
            process = await self.start_server()
            server = Server("gdrive-client")
            
            # Read the resource
            resource = Resource(f"gdrive:///{file_id}")
            content = await server.read_resource(resource)
            if process:
                process.terminate()
            return content
            
        except Exception as e:
            print(f"Error reading document: {e}")
            if process:
                process.terminate()
            return None

async def main():
    researcher = GDriveResearch()
    
    try:
        # Replace with your document name
        doc_name = "Research Document"  # Change this to match your document name
        print(f"Searching for document: {doc_name}")
        
        # Search for documents
        results = await researcher.search_document(doc_name)
        print("\nSearch results:")
        if isinstance(results, list):
            for result in results:
                print(f"- {result}")
            
            if results:
                # Get the first document's ID and read it
                doc_id = results[0].get('id')
                if doc_id:
                    print(f"\nReading document with ID: {doc_id}")
                    content = await researcher.read_document(doc_id)
                    if content:
                        print("\nDocument content:")
                        print(content)
                    else:
                        print("Could not read document content")
                else:
                    print("No document ID found in the search results")
        else:
            print("Unexpected search results format")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main()) 