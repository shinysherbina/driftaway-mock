Here are the steps for testing the application:

### Backend Testing

You can test each mocked MCP service individually to ensure they return the expected mock data. You can use a tool like `curl` or Postman for this.

1.  **Run the backend services** as described in the `README.md`.
2.  **Open a new terminal** and use the following `curl` commands to test each service:

    *   **Weather Service:**
        ```sh
        curl http://localhost:8089/weather/
        ```

    *   **Activities Service:**
        ```sh
        curl http://localhost:8081/activities/
        ```

    *   **Food Service:**
        ```sh
        curl http://localhost:8086/food/
        ```

    *   **Hotel Service:**
        ```sh
        curl http://localhost:8085/hotels/
        ```

    *   **Local Transport Service:**
        ```sh
        curl http://localhost:8083/local-transport/
        ```

    *   **Primary Transport Service:**
        ```sh
        curl http://localhost:8082/primary-transport/
        ```

    For each command, you should see a JSON response containing the mock data that was defined for that service.

### Frontend Testing

1.  **Run the frontend development server** as described in the `README.md`.
2.  **Open your web browser** and navigate to the URL provided by the Vite development server (usually `http://localhost:5173`).
3.  **Landing Page:** You should see the landing page with the destination input.
4.  **Trip Input Page:** Enter a destination and click "Start Planning". This will take you to the Trip Input page.
5.  **Trip Plan Page:** On the Trip Input page, click the "Generate Itinerary" button. This will navigate you to the Trip Plan page, where you should see the detailed mock itinerary, including weather, hotel, and daily activities.

### End-to-End Testing

For a complete end-to-end test, you would typically have the frontend make API calls to the backend. Since we have mocked the backend responses and the frontend is not yet making API calls, the end-to-end testing is simplified.

1.  **Run both the frontend and backend servers** simultaneously in separate terminals.
2.  **Perform the frontend testing steps** as described above.
3.  **Verify that the data displayed on the frontend** matches the mock data you have created. This confirms that the frontend is correctly consuming and displaying the mock data.
