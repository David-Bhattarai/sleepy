# Sleepy - AI Mental Health Companion

Sleepy is a web-based AI-powered application designed to provide mental health support. It functions as an empathetic companion, offering features like AI-driven chat, mood tracking, emotional intelligence analysis, goal setting, and relaxation exercises.

---

## How to Run This Project

This project is configured to run in two primary environments:

1.  **Project IDX (This IDE)**: Uses the integrated Nix environment.
2.  **GitHub Codespaces (or other Cloud Servers)**: Uses a standard Python `pip` environment, automated with a script.

### Method 1: Running in GitHub Codespaces (or other Linux Servers)

This is the recommended method for any standard cloud environment.

1.  **Push to GitHub**: Make sure your latest code, including `run_in_codespace.sh`, is pushed to your GitHub repository.
2.  **Open in Codespace**: Open your repository in a new GitHub Codespace.
3.  **Run the Automation Script**: Once the Codespace is loaded and you see the terminal, run the following single command:

    ```bash
    bash run_in_codespace.sh
    ```

That's it! The script will automatically:
*   Install system dependencies (`ffmpeg`).
*   Create a Python virtual environment.
*   Install all required Python packages.
*   Start the server.

You can then access the application using the URL provided in the **Ports** tab.

### Method 2: Running in Project IDX (This IDE)

This method is only for use within the Project IDX environment.

1.  **Configure Environment**: Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac), type **`Nix-Env: Re-evaluate Nix-file`**, and press `Enter`. Wait for the environment to build.
2.  **Run Server**: Once the environment is ready, open a new terminal and run:
    ```bash
    python3 server/app.py
    ```

---

## Core Technologies

- **Backend**: Python (Flask)
- **Frontend**: HTML, CSS, JavaScript
- **AI & Machine Learning**: DeepFace (for facial emotion recognition), VADER (for text sentiment analysis)
- **Environment Management**: Nix (for IDX), Pip (for standard environments)

## Features

-   **AI Therapist Chat**: An interactive, empathetic chatbot available 24/7.
-   **Sentiment Analysis**: Backend analysis of chat messages to detect user sentiment.
-   **Mood Tracker**: A tool for logging and monitoring daily mood.
-   **Emotional Intelligence Score**: A calculated score based on chat interactions.
-   **Goal Setting**: A feature to help users set and track wellness goals.
-   **Relaxation & Gaming Zone**: A collection of simple games and exercises.
-   **Video Chat**: AI Doctor consultation with real-time emotion detection.
-   **Secure Authentication**: User sign-up and sign-in system.
-   **Admin Panel**: A dashboard for application management.
