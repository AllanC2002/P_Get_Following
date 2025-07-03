# Get Following MicroService

This project is a backend application built with Flask, providing both RESTful and GraphQL APIs. It appears to manage user profiles and their following relationships.

## Backend Design Pattern

The application utilizes a **Layered Architecture**. This pattern organizes the codebase into distinct layers, each with a specific responsibility:

*   **Presentation/Routing Layer (`main.py`):** Handles incoming HTTP requests using Flask, directs them to appropriate handlers, and manages API endpoint definitions for both REST and GraphQL.
*   **Service Layer (`services/functions.py`, `resolvers/graphql_resolvers.py`):** Contains the core business logic.
    *   `services/functions.py`: Implements general business operations (e.g., fetching user followings).
    *   `resolvers/graphql_resolvers.py`: Provides specific logic for resolving GraphQL queries, often by calling functions in the `services` layer.
*   **Data Access Layer (`conections/mysql.py`):** Manages database connectivity.
*   **Data Model Layer (`models/models.py`):** Defines the application's data structures using SQLAlchemy ORM.

This layered approach promotes separation of concerns, making the application more maintainable and scalable.

## Communication Architecture

The application employs a **hybrid communication architecture**, supporting both:

1.  **REST API:** For specific, straightforward resource interactions.
2.  **GraphQL API:** For more flexible and complex data querying, allowing clients to request exactly the data they need.

## Folder Structure and Their Functions

The project follows a **Layer-Based Folder Pattern**, where directories are organized by their technical role:

*   **`.github/`**: Contains GitHub Actions workflow configurations.
    *   **`workflows/`**: Holds CI/CD pipeline definitions (e.g., `docker-publish.yml` for Docker image management).
*   **`conections/`**: Manages database connection logic.
    *   `mysql.py`: Sets up and provides connections to a MySQL database using SQLAlchemy.
*   **`models/`**: Defines the data models (ORM classes using SQLAlchemy) that map to database tables (e.g., `Profile`, `Followers`).
*   **`resolvers/`**: Contains GraphQL resolver functions that fetch data for the GraphQL schema fields, often utilizing the `services` layer.
*   **`schema/`**: Holds the GraphQL schema definition (`schema.graphql`), which outlines the types and operations available via the GraphQL API.
*   **`services/`**: Encapsulates the core business logic of the application (e.g., user-related operations like `get_following`).
*   **`tests/`**: Contains automated tests (unit, integration) for ensuring code quality and functionality.

Other important files in the root directory:
*   `main.py`: The main entry point for the Flask application.
*   `requirements.txt`: Lists project dependencies.
*   `dockerfile`: Instructions for building a Docker container for the application.
*   `.gitignore`: Specifies files and directories to be ignored by Git.

## API Endpoints

### Authentication

Both REST and GraphQL (when accessing protected fields) require JWT-based authentication. The token should be passed in the `Authorization` header with the `Bearer` scheme:

`Authorization: Bearer <YOUR_JWT_TOKEN>`

The JWT token is expected to contain a `user_id` field in its payload.

### REST API

1.  **Get Following List**
    *   **Endpoint:** `/following`
    *   **Method:** `GET`
    *   **Description:** Retrieves a list of users that the authenticated user is following.
    *   **Headers:**
        *   `Authorization: Bearer <YOUR_JWT_TOKEN>` (Required)
    *   **Success Response (200 OK):**
        ```json
        {
          "following": [
            {
              "Id_User": 2,
              "User_mail": "user2@example.com"
            }
            // ... more users
          ]
        }
        ```
    *   **Error Responses:**
        *   `401 Unauthorized`: Token issues (missing, invalid, expired).
        *   `404 Not Found`: Authenticated user's profile not found or inactive.

2.  **Root Endpoint**
    *   **Endpoint:** `/`
    *   **Method:** `GET`
    *   **Description:** A simple endpoint that returns a welcome message.
    *   **Success Response (200 OK):**
        ```
        Rest and GraphQl
        ```

### GraphQL API

*   **Endpoint:** `/graphql`
*   **Method:** `POST`
*   **Description:** Single endpoint for all GraphQL operations.
*   **Headers:**
    *   `Content-Type: application/json`
    *   `Authorization: Bearer <YOUR_JWT_TOKEN>` (Required for queries/fields that need authentication)
*   **Request Body:**
    A JSON object with a `query` field (and optional `variables`).
    ```json
    {
      "query": "...",
      "variables": { ... }
    }
    ```

*   **Available Queries:**

    1.  **Get Following List**
        *   **Query:**
            ```graphql
            query GetFollowing {
              following {
                Id_User
                User_mail
                # The schema (schema/schema.graphql) also defines:
                # Name
                # Lastname
                # Description
                # Id_preferences
                # Id_type
                # Status_account
                # Note: The current resolver (services/functions.py -> get_following)
                # only populates Id_User and User_mail for the 'following' list.
                # To retrieve other fields, the resolver implementation would need to be updated.
              }
            }
            ```
        *   **Description:** Retrieves a list of users that the authenticated user is following. Requires authentication.
        *   **Example Success Response (200 OK):**
            ```json
            {
              "data": {
                "following": [
                  {
                    "Id_User": 2,
                    "User_mail": "user2@example.com"
                  }
                  // ... more users
                ]
              }
            }
            ```
        *   **Example Error Response (e.g., 400 Bad Request):**
            If not authenticated or an error occurs in the resolver:
            ```json
            {
              "errors": [
                {
                  "message": "Not authenticated", // Or other relevant error
                  "locations": [ { "line": 2, "column": 3 } ],
                  "path": [ "following" ]
                }
              ]
            }
            ```
