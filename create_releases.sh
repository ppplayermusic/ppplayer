#!/bin/bash

# Create tag to trigger root release workflow
# Ensure the app repository CI has finished building and released v2.0.1 first!
git tag v2.0.1 HEAD
git push origin v2.0.1
