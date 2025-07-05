**You should change the content of this file. Please use all second-level headings.**

# Installation Guide

## Prerequisites

You will need:
* Python 3.x
* Node.js and npm\pnpm
* MongoDB

## Installation Steps

**1. Clone the repository:**

```bash
git clone git@github.com:strawberrySword/hermes.git
cd hermes
```

**2. Set up the backend:**
- **Install Python dependencies:**
  ```bash
  pip install -r server/requirements.txt
  ```

- **Set up environment variables:**
  Create a `.env` file in the `server` directory and add the following:
  The bottom three env variables are from auth0. You will need to set up an auth0 account.
  ```
    mongodb://127.0.0.1:27017/
    AUTH0_DOMAIN=
    API_AUDIENCE=
    ALGORITHMS=RS256
  ```

- **Manual DB seed:**
  We have provided `setup/hermes.articles.json` which is a dump of the articles collection.
  Create a new db under the name `hermes` and load the `articles` collection.

- **Run the server:**
  ```bash
  python3 server/app.py
  ```
  The server will start on `http://localhost:5000`.

**3. Set up the frontend:**

- **Install Node.js dependencies:**
  ```bash
  cd client
  npm install
  ```

- **Run the client:**
  ```bash
  npm run dev
  ```
  The client will be available at `http://localhost:5173`.
