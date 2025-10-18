#!/bin/bash
# Auto-link latest index as default

echo "Setting up automatic index linking..."

# Create a monitoring script in the container
docker exec rfp-agent-backend-1 sh -c "cat > /auto_link_indexes.sh << 'EOF'
#!/bin/sh
while true; do
  # Find the most recently modified index directory
  LATEST_INDEX=\$(ls -td /app/indexes/*/ 2>/dev/null | grep -v '/default' | head -1)

  if [ ! -z \"\$LATEST_INDEX\" ]; then
    # Remove trailing slash
    LATEST_INDEX=\${LATEST_INDEX%/}

    # Check if it has actual index files
    if [ -f \"\$LATEST_INDEX/index.faiss\" ]; then
      # Update the default symlink
      rm -f /app/indexes/default
      ln -sf \$LATEST_INDEX /app/indexes/default
      echo \"Linked \$LATEST_INDEX as default\"
    fi
  fi

  # Wait 30 seconds before checking again
  sleep 30
done
EOF"

# Make it executable and run in background
docker exec -d rfp-agent-backend-1 sh -c "chmod +x /auto_link_indexes.sh && /auto_link_indexes.sh"

echo "✅ Auto-linking enabled. Latest index will be set as default every 30 seconds."