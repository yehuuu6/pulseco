#!/bin/bash

# Run this script in your terminal to compile plugin modules with Nuitka.
# Ensure you have installed Nuitka and its dependencies.
# Usage: You can either run this script directly or use the Pulse CLI tool by executing python pulse.py build:plugins

SRC_DIR="app/plugins"
BUILD_DIR="build/plugins"

mkdir -p "$BUILD_DIR"

for file in "$SRC_DIR"/*.py; do
    base=$(basename "$file" .py)
    if [[ "$base" != "__init__" ]]; then
        echo "Compiling $file -> $BUILD_DIR/${base}.so"
        
        # Compile with Nuitka
        python3 -m nuitka --module "$file" \
            --output-dir="$BUILD_DIR" \
            --remove-output
        
        # Clean up and rename
        cd "$BUILD_DIR"
        
        # Find the actual .so file created by Nuitka (with full suffix)
        actual_so_file=$(find . -name "${base}.cpython-*.so" | head -1)
        
        if [[ -n "$actual_so_file" ]]; then
            # Rename to simple .so extension
            mv "$actual_so_file" "${base}.so"
            echo "Renamed $actual_so_file to ${base}.so"
        fi
        
        # Remove all other files except the renamed .so file
        find . -name "${base}.*" ! -name "${base}.so" -delete
        
        # Remove any directories created by Nuitka
        find . -type d -name "${base}.*" -exec rm -rf {} + 2>/dev/null || true
        
        cd - > /dev/null
    fi
done