# Fame Application

This application generates random responses based on a list of famous persons in science. It uses the OpenAI API to generate these responses.

## Prerequisites

- Python 3.8
- Docker
- An OpenAI API key

## Setup

1. Clone this repository to your local machine.
2. Navigate to the directory containing the application.

## Running the Application with Docker

1. Build the Docker image:

    ```
    docker build -t ScientistSpotlight .
    ```

2. Run the Docker container, passing in your OpenAI API key as an environment variable and mapping a volume to the `/app` directory in the container:

    ```
    docker run -e OPENAI_API_KEY=your_openai_api_key -v /path/to/your/host/directory/fame_persons.txt:/app/fame_persons.txt ScientistSpotlight
    ```

    Replace `your_openai_api_key` with your actual OpenAI API key, and `/path/to/your/host/directory` with the path to the directory on your host machine where you want the `fame_persons.txt` file to be written.

When you run the application, it will generate a random response and write the name of the famous person to the `fame_persons.txt` file in the specified directory on your host machine.