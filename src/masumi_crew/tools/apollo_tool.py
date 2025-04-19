from crewai.tools import BaseTool
from typing import Type, List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json
from composio_crewai import ComposioToolSet, App


class ApolloSearchInput(BaseModel):
    """Input schema for ApolloSearchTool."""
    query: str = Field(..., description="The search query to find people in Apollo.")
    limit: Optional[int] = Field(10, description="Maximum number of results to return.")


class ApolloSearchTool(BaseTool):
    name: str = "Apollo People Search"
    description: str = (
        "Search for people using Apollo's database. Useful for finding professionals, "
        "investors, or decision-makers in specific industries or companies."
    )
    args_schema: Type[BaseModel] = ApolloSearchInput

    def _run(self, query: str, limit: int = 3) -> str:
        # Initialize the Apollo toolset
        toolset = ComposioToolSet()
        tools = toolset.get_tools(apps=[App.APOLLO])
        
        # Use the Apollo search tool
        apollo_tool = tools[0]  # Assuming the first tool is the search tool
        
        # Execute the search
        result = apollo_tool.run(query=query, limit=limit)
        
        # Apollo API key for enrichment
        api_key = "l-UG2w5z1LeZOzJya2JWBg"

        # Endpoint for people match
        url = "https://api.apollo.io/api/v1/people/match?reveal_personal_emails=true"

        # Set up headers
        headers = {
            "accept": "application/json",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "x-api-key": api_key
        }
        return json.dumps(result, indent=2) 