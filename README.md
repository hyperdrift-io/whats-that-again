# WhatsThatAgain

A minimal application that helps you remember things that are on the tip of your tongue by directly querying AI.

## Features

- Simple, clean interface
- Conversation history to refine your search
- Memory tags for better recall
- Automatic model progression for difficult questions
- Daily query limits to control costs

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Svelte + TypeScript
- **Build Tool**: Bun (JavaScript runtime & package manager)
- **AI**: Anthropic's Claude API

## Getting Started

### Prerequisites

- Python 3.12+
- Bun (JavaScript runtime & package manager)
- Anthropic API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/whatsthat.git
   cd whatsthat-fastapi-svelte
   ```

2. Set up the backend:
   ```
   cd api
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the `api` directory with your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your-key-here
   ```

4. Set up the frontend:
   ```
   cd ../frontend
   bun install
   ```

### Running the Application

1. Start the backend server:
   ```
   cd api
   uvicorn main:app --reload
   ```

2. In a separate terminal, start the frontend development server:
   ```
   cd frontend
   bun run dev
   ```

3. Open your browser and navigate to `http://localhost:5173`

### Building for Production

1. Build the frontend:
   ```
   cd frontend
   bun run build
   ```

2. The built files will be in the `frontend/dist` directory, which the FastAPI server will serve automatically.

3. Run the production server:
   ```
   cd api
   uvicorn main:app
   ```

## Deployment

### Deploying to Render.com

This project includes a `render.yaml` configuration file for easy deployment to Render.com:

1. Create a Render.com account if you don't have one
2. Fork or push this repository to GitHub
3. In Render Dashboard, click "New" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and set up the services
6. Add your `ANTHROPIC_API_KEY` as an environment variable for the backend service
7. Deploy!

Alternatively, you can deploy the services separately:

#### Backend API (FastAPI)
- Create a "Web Service"
- Connect your GitHub repository
- Set build command: `pip install -r api/requirements.txt`
- Set start command: `cd api && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add environment variable: `ANTHROPIC_API_KEY=your-key-here`

#### Frontend (Svelte + Bun)
- Create a "Static Site"
- Connect your GitHub repository
- Set build command: `cd frontend && curl -fsSL https://bun.sh/install | bash && ~/.bun/bin/bun install && ~/.bun/bin/bun run build`
- Set publish directory: `frontend/dist`

## License

MIT 