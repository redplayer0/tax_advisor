# tax_advisor
### ![Test status](https://github.com/redplayer0/tax_advisor/actions/workflows/backend-tests.yml/badge.svg)
Proof of concept app that provides tax advice. FastAPI | Angular 19 | sqlite | Docker | oath2 | openAPI

# Setup - How to run
- Clone the repo
- In order to run the application you need an `.env` file, for convenience an example is provided
- Run 'mv .example_env .env' to rename the example, then open the file and edit the values with your keys and preferences
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
- This data along with a developer message that guides the model how to respond, is then passed to the OpenAI model via the client.chat.completions.create method. The prompt includes tax-related questions, and the model is instructed to provide tax advice based on the user's financial details.
- The app sends the input data to the OpenAI API in the form of a chat prompt. The model receives a request that combines a tax-related instruction with the user's financial data.
- The OpenAI model responds with the generated tax advice. The response is then saved to the database, along with the user’s input.
- The model's response is stored in a new Advice object, which also includes the user's original input for reference. This is then returned to the user via the API.
- The /advice endpoint responds with the saved advice, including both the user’s financial data and the AI-generated tax advice.
- The advice contains user-specific tax information and suggestions, helping users understand their tax situation based on their financial details.

# Docker
- Both backend and frontend parts of the application are containerized
- The backend is served through `uvicorn` while the frontend is using `nginx` to serve the static files
- We are using a docker-compose to run the application as a whole with one command
- Our keys are saved in a .env file in the projects root and are kept out of version control

# CI/CD
The CI pipeline automatically runs tests on the backend whenever changes are pushed to the main branch. The steps are:
- Code Checkout: The workflow starts by checking out the latest code from the repository
- Dependencies Installation: It sets up the necessary environment and installs the required dependencies
- Run Tests: The backend tests are executed using pytest to ensure that everything works as expected
- Test Status: After running the tests, the pipeline will show whether they have passed or failed
