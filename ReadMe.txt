# Mew 🐈 : Local RAG implementation and personal assistant ! (= ФェФ=) **

## Introduction

**Mew** is a local implementation of a Retrieval-Augmented Generation (RAG) solution, designed as a personal assistant powered by efficient **gguf models**. Using **Ollama** technology, Mew delivers a streamlined and private assistant experience that runs entirely on your local machine, ensuring privacy and quick responses without relying on external servers.

## How It Works

Mew operates with three main components:

1. **Backend** - Handles core functionalities and orchestrates data flow.
2. **Frontend** - Provides an intuitive interface for user interactions.
3. **Ollama Server** - Powers the assistant with language model processing.

These components interact seamlessly, allowing for real-time responses from Mew.

## Setup

### Prerequisites

Before setting up Mew, ensure you have the following:

- A **processor** capable of running gguf models (refer to relevant webpages for model compatibility).
- **Python** installed.
- **Visual Studio Code** (or any other IDE) for an enhanced development experience.
- Compatible with **Linux** and **Windows** (Mac compatibility unknown).

### Setting up the Environment

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Install Dependencies**: Use `requirements.txt` to install the necessary packages.
   ```bash
   pip install -r requirements.txt
```

### How to Use Mew

1. Download a gguf Model: Obtain a gguf model compatible with Ollama.
2. Place Model in the ```models``` Folder: Move the downloaded model into the models directory within your repository.
3. Start the Server: Run the following command to start the server
 ```bash
   python init_server.py
```
4. Launch the Application: Use Uvicorn to start the app:
 ```bash
   uvicorn run:app mew_app
```


Once the setup is complete, Mew will be up and running. Enjoy your new personal assistant!