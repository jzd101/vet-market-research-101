from mcp.server.fastmcp import FastMCP

# Create an MCP server instance
mcp = FastMCP("Vet Market Researcher")

@mcp.tool()
def search_vet_market_data(query: str) -> str:
    """
    Searches for veterinary market data.
    Useful for finding market size, trends, and growth from 2020-2025.

    Args:
        query: The search query string.
    """
    # In a real scenario, this would call a search API like Tavily or Google.
    # For this POC, we return high-quality mock data as requested.

    # We can simulate different responses based on the query if needed,
    # but for now, we return the core dataset.

    return """
    **Veterinary Market Overview (2020-2025)**

    *   **Global Market Size:**
        *   2020: Valued at approx. $44.5 Billion USD.
        *   2025 (Projected): Expected to reach $68.5 Billion USD.
        *   CAGR: ~9% during the forecast period.

    *   **Key Drivers:**
        *   Rising pet ownership (especially dogs and cats).
        *   Increased spending on animal health and pet insurance.
        *   Technological advancements in veterinary diagnostics.
        *   Humanization of pets leading to premium care demand.

    *   **Regional Trends:**
        *   **North America:** Dominates the market due to high pet adoption and advanced healthcare infrastructure.
        *   **Asia-Pacific:** Fastest growing region, driven by rising disposable income in China and India.

    *   **Segment Analysis:**
        *   **Diagnostics:** High growth area with new point-of-care devices.
        *   **Therapeutics:** Vaccines and parasiticides remain top revenue generators.
        *   **Telehealth:** Emerging trend for remote consultation.
    """

if __name__ == "__main__":
    # This entry point allows running the server directly
    mcp.run()
