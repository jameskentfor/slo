FROM mcr.microsoft.com/devcontainers/python:3-3.14-trixie

# Set `DEVCONTAINER` environment variable to help with orientation
ENV DEVCONTAINER=true

# Create directories and set ownership (combined for fewer layers)
RUN mkdir -p /commandhistory /workspace /home/vscode/.claude && \
  touch /commandhistory/.bash_history && \
  chown -R vscode:vscode /commandhistory /workspace /home/vscode/.claude
  
WORKDIR /workspace

USER vscode

# Set PATH early so claude and other user-installed binaries are available
ENV PATH="/home/vscode/.local/bin:$PATH"

# Install Claude Code natively with marketplace plugins
RUN curl -fsSL https://claude.ai/install.sh | bash