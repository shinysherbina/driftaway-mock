# Driftaway Mock

This is a mock-only version of the Driftaway Trip Planner application.

## Running the Application

To run the application, you need to have Node.js and Python installed.

### Frontend

1.  Navigate to the `frontend` directory:
    ```sh
    cd frontend
    ```
2.  Install the dependencies:
    ```sh
    npm install
    ```
3.  Run the development server:
    ```sh
    npm run dev
    ```

### Backend Setup with Virtual Environment

1.  **Create a virtual environment:**

    ```sh
    python -m venv .venv
    ```

2.  **Activate the virtual environment:**

    *   **On Windows:**
        ```sh
        .venv\Scripts\activate
        ```
    *   **On macOS and Linux:**
        ```sh
        source .venv/bin/activate
        ```

3.  **Install the dependencies:**

    ```sh
    cd backend
    pip install -r requirements.txt
    ```

4.  **Run the main application:**

    ```sh
    python main.py
    ```

This will start all the mock MCP services.
