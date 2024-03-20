# neuro-gen
AI generated images service 

## Stack
`Python` `Fastapi` `Pydantic` `SQLAlchemy` `Alembic` `Asyncio` `Uvicorn` `Docker` `PostgreSQL` 

## Features

- Utilizes the FastAPI framework for generating images using an external API service (Kandinsky).
- Includes routers for versioned endpoints.
- Defines Pydantic models for request and response handling.
- Manages database models for SQLAlchemy.
- Provides asynchronous database methods for handling image data.

## Installation

1. Clone the only docker-compose.yml from repository:

2. Create a `.env` file in the root directory of the project and add the necessary environment variables as .env.example. Retrieve API_KEY and SECRET_KEY: https://fusionbrain.ai/.

3. Ensure you have Docker and Docker Compose installed on your system.

4. Run the following command to start the application using Docker Compose:
   ```
   docker-compose up -d
   ```

5. Once the application is running, you can access the API endpoints through your web browser or API client. Openapi documentation is available at http://localhost:8008/docs/.

## API Endpoints

- **Version 1 Endpoints** (provided by `v1_router`):
  - **POST `/v1/image`**: Handles image-related requests.
    - **Request Parameters**:
      - `title`: Title of the image.
      - `name`: Name of the image.
      - `id`: ID of the image.
    - **Request Body**: Expects a JSON object with one of the following fields: `title`, `name`, or `id`.
    - **Response**: Returns the base64 encoded image data.
    - **Error Handling**:
      - Returns a 400 error if the request does not include a valid field (`title`, `name`, or `id`).
      - Returns a 404 error if the image does not exist.
      - Returns a 418 error with its desciption if there is any problem with Kandinsky service.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository and submit a pull request.