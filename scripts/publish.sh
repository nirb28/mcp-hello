#!/bin/bash

curl -X POST \
  -H "Content-Type: application/json" \
  --data-binary @mcp-server.json \
  http://localhost:8080/v0/publish
