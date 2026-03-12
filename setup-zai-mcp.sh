#!/bin/bash
# Z.AI MCP Tools Setup Script for Trae IDE

echo "🚀 Setting up Z.AI MCP Tools for Trae IDE..."

# Set API key
export Z_AI_API_KEY=46a64e2930834d52afc6d0ce9bb4e0f1.nDGd72qVUwaanyB7

# Install Z.AI MCP packages globally
echo "📦 Installing Z.AI MCP packages..."
npm install -g @z-ai/vision-mcp @z-ai/search-mcp @z-ai/reader-mcp

# Create startup script
cat > start-zai-mcp.sh << 'EOF'
#!/bin/bash
# Start Z.AI MCP servers

echo "Starting Z.AI MCP servers..."

# Start Vision MCP server in background
echo "Starting Vision MCP server..."
npx -y @z-ai/vision-mcp &
VISION_PID=$!

# Start Search MCP server in background  
echo "Starting Search MCP server..."
npx -y @z-ai/search-mcp &
SEARCH_PID=$!

# Start Reader MCP server in background
echo "Starting Reader MCP server..."
npx -y @z-ai/reader-mcp &
READER_PID=$!

echo "✅ Z.AI MCP servers started!"
echo "Vision PID: $VISION_PID"
echo "Search PID: $SEARCH_PID" 
echo "Reader PID: $READER_PID"

# Save PIDs for later management
echo "$VISION_PID $SEARCH_PID $READER_PID" > .zai-mcp-pids

# Wait for interrupt
trap "kill $VISION_PID $SEARCH_PID $READER_PID; exit" INT
wait
EOF

chmod +x start-zai-mcp.sh

# Create stop script
cat > stop-zai-mcp.sh << 'EOF'
#!/bin/bash
# Stop Z.AI MCP servers

if [ -f .zai-mcp-pids ]; then
    echo "Stopping Z.AI MCP servers..."
    kill $(cat .zai-mcp-pids) 2>/dev/null
    rm .zai-mcp-pids
    echo "✅ Z.AI MCP servers stopped!"
else
    echo "No MCP servers running or PID file not found"
fi
EOF

chmod +x stop-zai-mcp.sh

echo "✅ Setup complete!"
echo ""
echo "To start Z.AI MCP tools:"
echo "  ./start-zai-mcp.sh"
echo ""
echo "To stop Z.AI MCP tools:"
echo "  ./stop-zai-mcp.sh"
echo ""
echo "Your Z.AI API key is configured and ready to use in Trae IDE!"