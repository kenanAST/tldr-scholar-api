# tldr-scholar-api

This project serves as the backend API for summarizing academic articles using LLMs (Large Language Models) and CrewAI.

## Installation and Usage

### Step 1: Activate Conda Environment and Install Python 3.10

First, ensure you have Conda installed. If not, follow the installation instructions at [Conda Documentation](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

```bash
conda create --name myenv python=3.10
conda activate myenv
```

### Step 2: Install Dependencies
Install the required Python packages using the provided requirements.txt file.

`pip install -r requirements.txt`

### Step 3: Setup Environment Variables
Create a .env file in the root directory of the project and add the following variables with appropriate values:
```
OPENAI_API_KEY=zPz5x6Db7A8cJLk3Vc0Fj2Lg3Dv8Mn9Jk0OoHsBd7Fn8Wf4Mk9
BROWSERLESS_API_KEY=c87b2f98-a0c1-4c87-bc2a-9c8b1d3e8c4f
SERPER_API_KEY=78e9a4b1c87d20a8e4f23d95e9b32cf17a84e9a3
```

### Step 4: Run the Application
Execute the main script main.py to start the application.
`python main.py`

