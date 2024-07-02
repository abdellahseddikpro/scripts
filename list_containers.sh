#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <namespace-regex-pattern>"
    exit 1
fi

NAMESPACE_REGEX=$1

# Get the namespaces that match the regex pattern
NAMESPACES=$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep -E "$NAMESPACE_REGEX")

if [ -z "$NAMESPACES" ]; then
    echo "No namespaces found matching the pattern: $NAMESPACE_REGEX"
    exit 1
fi

# Iterate over the matched namespaces
for NAMESPACE in $NAMESPACES; do
    echo "Namespace: $NAMESPACE"
    # Get all pods in the current namespace
    PODS=$(kubectl get pods -n $NAMESPACE -o jsonpath='{.items[*].metadata.name}')
    
    for POD in $PODS; do
        echo "  Pod: $POD"
        # Get containers in the current pod
        CONTAINERS=$(kubectl get pod $POD -n $NAMESPACE -o jsonpath='{.spec.containers[*].name}')
        IMAGES=$(kubectl get pod $POD -n $NAMESPACE -o jsonpath='{.spec.containers[*].image}')
        
        IFS=' ' read -r -a CONTAINER_ARRAY <<< "$CONTAINERS"
        IFS=' ' read -r -a IMAGE_ARRAY <<< "$IMAGES"
        
        for i in "${!CONTAINER_ARRAY[@]}"; do
            echo "    Container Name: ${CONTAINER_ARRAY[$i]}"
            echo "    Image: ${IMAGE_ARRAY[$i]}"
        done
    done
done
