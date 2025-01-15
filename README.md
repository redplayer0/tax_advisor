# tax_advisor
Proof of concept app that provides tax advice. FastAPI | Angular 19 | sqlite | Docker | oath2 | openAPI

# Setup - How to run
- Clone the repo
- Create a .env file in the repo's root, with the following variables  SECRET_KEY, OPEN_API_KEY, HASH_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINS
- Run `docker-compose up --build`
- Navigate to `localhost:80` or `0.0.0.0:80`
- Explore the application

# Backend application
- fastapi application
- sqlite database for storage
- OAuth2 for authentication with jwt token
- connect to openAI using the SDK
- user can create account
- user provides financial info and a prompt and the app return tax advise through the use of gpt-4o

# REST API
- POST /token: Login with username and password to get an access token (OAuth2).
- POST /signup: Create a new user with a username and password.
- GET /users/me: Get the current user's details (requires Bearer token).
- POST /advice: Generate financial advice based on user input (requires Bearer token).

# openAI API Integration
- The OpenAI API key is loaded securely from the environment variables using the dotenv package.
- The OpenAI client is initialized with this key to make authenticated requests to the OpenAI API.
- The /advice endpoint accepts a POST request where users send their financial information. This data is captured in an AdviceBase object.
- This data is then passed to the OpenAI model via the client.chat.completions.create method. The prompt includes tax-related questions, and the model is instructed to provide tax advice based on the user's financial details.
- The app sends the input data to the OpenAI API in the form of a chat prompt. The model receives a request that combines a tax-related instruction with the user's financial data.
- The prompt instructs the model to give detailed yet concise advice, focusing on the user's tax situation, with relevant sources when possible.
- The OpenAI model responds with the generated tax advice. The response is then saved to the database, along with the user’s input.
- The model's response is stored in a new Advice object, which also includes the user's original input for reference. This is then returned to the user via the API.
- The /advice endpoint responds with the saved advice, including both the user’s financial data and the AI-generated tax advice.
- The advice contains user-specific tax information and suggestions, helping users understand their tax situation based on their financial details.
