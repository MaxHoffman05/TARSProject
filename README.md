# TARS Project

> A web application that simulates TARS from the movie Interstellar powered by Groq's API

## Overview

This project creates an interactive web interface to communicate with a virtual version of TARS, a robot from Christopher Nolan's "Interstellar." Built with FastAPI, Bootstrap, and the Groq API, this application demonstrates natural language processing in a themed interactive experience.

## Technologies Used

- **Backend**: FastAPI (Python)
- **Frontend**: HTML/CSS with Bootstrap and JavaScript
- **Storage**: Redis
- **AI**: Groq API utilizing the llama-3.3-70b-versatile model

## Setup

### Prerequisites

- Python 3.8+ (I used 3.10.12)
- Redis
- Groq API Key (Free with limits)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/MaxHoffman05/TARSProject
```

2. **Set up virtual environment**
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   - Create a `.env` file in the project root

     - Add your Groq API key:

       ```
       GROQ_API_KEY=your_api_key_here
       ```

     - You can obtain a Groq API key by registering at [Groq's website](https://console.groq.com/keys)

     - While in the `.env` file you will also want to add the frontend url:

       ```
       FRONT_END_URL=your_url_here
       ```

     - This is used by FastAPI when connecting to the front end.

   - You will also want to create a `config.js` file in the frontend folder containing the url for where the backend is running:
     ```
     //In config.js
     export const BACKEND_URL = "your url here";
     ```

5. **Start Redis server**

```bash
   sudo service redis-server start
```

7. **Run the Application**

```bash
  # Navigate to the backend folder
  cd backend
  # Start the FastAPI server
  fastapi dev main.py
```

You can also start the backend by running the bash script below:

```bash
   # Give permission
   chmod +x ./server.sh
   # Run script
   ./server.sh
```

8. **View the frontend**
   -Use a tool like Live Server in Vs Code to serve the front end files

## Storage

You can run the command below to enter the Redis Cli to view variables

```bash
    redis-cli
```

To view what's being stored

```bash
   lrange chat_history 0 -1
```

## API Documentation

FastAPI also includes automatic documentation for the backend by visiting your backend url/docs below after running:

```
By default
http://localhost:8000/docs
```

## Project Structure

```
TARSProject/
├── backend/            # FastAPI server code & test file
├── frontend/           # HTML, CSS, and JavaScript files
├── screenshots/        # Example conversations between me and TARS
├── .env                # Environement Variables
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── server.sh           # Script to start FastAPI
```

## About

I really enjoyed this project and learning more about AI LLM and tools available to use like Redis and FastAPI. During this project I learned...

- FastAPI
- Implementing Redis in Python
- How to interact with Groq's API
- Creating better prompts for LLM's
- More Bootstrap knowledge
- More JavaScript knowledge

## Example Output

Below is a collection of my favorite TARS interactions

<div style="text-align: center;">
   <img src="./screenshots/case.png" style="padding: 20px;">

   <img src="./screenshots/spacetime.png" style="padding: 20px;">

   <img src="./screenshots/pizza.png" style="padding: 20px;">

   <img src="./screenshots/spongebob.png" style="padding: 20px;">
</div>

I encourage you to ask TARS questions!
