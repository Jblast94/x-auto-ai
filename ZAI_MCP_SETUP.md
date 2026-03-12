# Z.AI MCP Tools Configuration for Trae IDE

## Installation

Install the Z.AI MCP packages:
```bash
npm install -g @z-ai/vision-mcp @z-ai/search-mcp @z-ai/reader-mcp
```

## Configuration

Your Z.AI API key is: `46a64e2930834d52afc6d0ce9bb4e0f1.nDGd72qVUwaanyB7`

## MCP Servers Available:

### 1. Vision MCP Server
- **Package**: `@z-ai/vision-mcp`
- **Purpose**: Image analysis, vision tasks
- **Usage**: Analyze images, extract text, detect objects

### 2. Search MCP Server  
- **Package**: `@z-ai/search-mcp`
- **Purpose**: Web search functionality
- **Usage**: Search for information, get real-time data

### 3. Reader MCP Server
- **Package**: `@z-ai/reader-mcp`
- **Purpose**: Read and process web content
- **Usage**: Extract content from URLs, process documents

## Trae IDE Integration

To use these tools in Trae IDE:

1. **Set environment variable**:
   ```bash
   export Z_AI_API_KEY=46a64e2930834d52afc6d0ce9bb4e0f1.nDGd72qVUwaanyB7
   ```

2. **Start MCP servers**:
   ```bash
   # Vision server
   npx -y @z-ai/vision-mcp
   
   # Search server  
   npx -y @z-ai/search-mcp
   
   # Reader server
   npx -y @z-ai/reader-mcp
   ```

3. **In Trae IDE**, you can now use commands like:
   - `Analyze this image: [image_url]`
   - `Search for: [query]`
   - `Read this URL: [url]`

## Available Tools

- **Image Analysis**: Analyze images, extract text, detect NSFW content
- **Web Search**: Get current information, search trends
- **Content Reading**: Extract and process web content
- **Vision Tasks**: OCR, object detection, image description

## Example Usage in Trae IDE

```
# Analyze an image
Analyze this image: https://example.com/image.jpg

# Search for information  
Search for: latest AI trends 2025

# Read web content
Read this URL: https://docs.z.ai

# Extract text from image
Extract text from: https://example.com/document.png
```