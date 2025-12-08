#!/bin/bash
# lib/detect-metadata.sh - Repository metadata detection library

# Check if jinja2-cli is available
check_dependencies() {
    if ! command -v jinja2 &> /dev/null; then
        echo "Error: jinja2-cli is required but not found" >&2
        echo "Install with: brew install jinja2-cli" >&2
        return 1
    fi
}

# Extract metadata from repository path and contents
detect_repo_metadata() {
    local repo_path="$1"
    local repo_name=$(basename "$repo_path")
    
    # Initialize metadata
    local client=""
    local platform=""
    local cloud_provider=""
    local language=""
    local repo_type=""
    
    # Extract client from path: /Data/GIT/{CLIENT}/...
    if [[ "$repo_path" =~ /Data/GIT/([^/]+)/ ]]; then
        client="${BASH_REMATCH[1]}"
    fi
    
    # Extract platform from path: /Data/GIT/{CLIENT}/{PLATFORM}/...
    if [[ "$repo_path" =~ /Data/GIT/[^/]+/([^/]+)/ ]]; then
        platform="${BASH_REMATCH[1]}"
    fi
    
    # Detect cloud provider from path or repo name
    case "$repo_path" in
        *aws*|*-aws-*) cloud_provider="aws" ;;
        *azure*|*azurerm*|*-azurerm-*) cloud_provider="azure" ;;
        *gcp*|*google*|*-google-*) cloud_provider="gcp" ;;
        *oci*|*-oci-*) cloud_provider="oci" ;;
    esac
    
    # Detect language from files in repository
    if [[ -f "$repo_path/main.tf" || -f "$repo_path/variables.tf" || $(find "$repo_path" -name "*.tf" -type f 2>/dev/null | head -1) ]]; then
        language="terraform"
    elif [[ -f "$repo_path/package.json" ]]; then
        language="javascript"
    elif [[ -f "$repo_path/requirements.txt" || -f "$repo_path/pyproject.toml" ]]; then
        language="python"
    elif [[ -f "$repo_path/pom.xml" ]]; then
        language="java"
    elif [[ -f "$repo_path/go.mod" ]]; then
        language="go"
    elif [[ -f "$repo_path/Cargo.toml" ]]; then
        language="rust"
    elif [[ -f "$repo_path/Package.swift" ]]; then
        language="swift"
    fi
    
    # Detect repository type
    case "$repo_name" in
        terraform-*-*) repo_type="terraform-module" ;;
        *-template) repo_type="template" ;;
        *-api|*-service) repo_type="application" ;;
        *-library|*-lib) repo_type="library" ;;
        *) repo_type="general" ;;
    esac
    
    # Export metadata as environment variables
    export REPO_CLIENT="$client"
    export REPO_PLATFORM="$platform" 
    export REPO_CLOUD_PROVIDER="$cloud_provider"
    export REPO_LANGUAGE="$language"
    export REPO_TYPE="$repo_type"
    export REPO_NAME="$repo_name"
    export REPO_PATH="$repo_path"
    
    # Return JSON metadata
    cat << EOF
{
    "client": "$client",
    "platform": "$platform",
    "cloud_provider": "$cloud_provider",
    "language": "$language",
    "repo_type": "$repo_type",
    "repo_name": "$repo_name",
    "repo_path": "$repo_path"
}
EOF
}

# Render Jinja2 template with metadata
render_template() {
    local template_file="$1"
    local output_file="$2"
    
    # Create JSON data for jinja2-cli
    local data_json=$(cat << EOF
{
    "client": "$REPO_CLIENT",
    "platform": "$REPO_PLATFORM", 
    "cloud_provider": "$REPO_CLOUD_PROVIDER",
    "language": "$REPO_LANGUAGE",
    "repo_type": "$REPO_TYPE",
    "repo_name": "$REPO_NAME",
    "repo_path": "$REPO_PATH"
}
EOF
    )
    

    
    # Render template using jinja2-cli
    echo "$data_json" | jinja2 "$template_file" > "$output_file"
    
    echo "✅ Generated $(basename "$output_file")"
}