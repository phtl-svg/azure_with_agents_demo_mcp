#!/bin/bash
# =============================================================================
# startup.sh — Azure App Service Linux startup script
# =============================================================================
#
# WHY THIS FILE EXISTS (and why it replaces web.config):
#
# On Windows, IIS (a Microsoft web server) sits in front of your Python process.
# IIS needs a "web.config" XML file to know how to launch your app.
#
# On Linux, there is NO IIS. Azure runs your Python process directly inside
# a container. There is no intermediary web server — your app IS the web server.
# Azure just needs to know one thing: what shell command starts your app.
# That command goes here.
#
# HOW THE PORT WORKS ON LINUX (different from Windows!):
#
# On Windows, IIS assigned a random internal port via %HTTP_PLATFORM_PORT%.
# On Linux App Service, Azure sets a single environment variable called PORT.
# Its default value is 8000. Your app must listen on that port.
#
# The syntax ${PORT:-8000} means:
#   "use the value of $PORT, but if PORT is not set, fall back to 8000"
# This makes the script safe to run locally too (where PORT may not be set).
#
# HOW AZURE CALLS THIS FILE:
# This script is registered as the "startup command" in the Azure Portal
# (Configuration → General settings → Startup Command: bash startup.sh)
# OR via the GitHub Actions workflow's startup-command parameter.
# Azure runs this from your app's root directory (/home/site/wwwroot).
#
# VIRTUAL ENVIRONMENT ON LINUX:
# When Azure's Oryx build system installs your dependencies, it creates a
# virtual environment at /tmp/8d.../antenv (a temp path). It automatically
# activates that venv before running this startup script, so all packages
# from requirements.txt are available to this python/uvicorn process.
# =============================================================================

uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
