# Driftaway Backend

This directory contains the backend code for the Driftaway trip planning assistant.

## Mock Server

For frontend development and testing, a mock server is provided that simulates the backend API without requiring external services or API keys. It returns hardcoded data for a trip to Kyoto.

### Setup and Running

1.  **Install Dependencies**: Before running the mock server for the first time, ensure you have installed the required Python packages. From the root directory of the project, run:

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Server**: Navigate to the `backend` directory and run the mock server using the following command:

    ```bash
    python mock_main.py
    ```

3.  **Access the API**: The mock server will be running at `http://localhost:8000`. You can now point your frontend application to this address to interact with the mock API.
