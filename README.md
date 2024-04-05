# LangChain RAG with Azure AI Search

This repository contains a Streamlit application that generates project ideas based on Microsoft Azure Certifications and the level of the project (beginner, intermediate, advanced). The application uses the LangChain RAG (Retrieval-Augmented Generation) model with Azure AI Search to generate the project ideas.

## Features

- Select a Microsoft Azure Certification from a dropdown list (AZ-900, AZ-104, AZ-305, AZ-400).
- Select a project level from a dropdown list (beginner, intermediate, advanced).
- Generate a detailed project idea, including the project name, description, list of services used, and steps to make the project.

## Setup

- Clone this repository.
- Create a [virtual environment.](https://docs.python.org/3/library/venv.html)
- Install the required Python packages:

``` python
pip install -r requirements.txt
```

- Set up your Azure AI Search service and get your endpoint URL and admin key.
- Set up your OpenAI API key.
- Create a .env file in the root directory of the project and add your Azure Search endpoint URL, admin key, and OpenAI API key (look at the `.env.example):

``` bash
AZURE_SEARCH_ENDPOINT="<YOUR_AZURE_SEARCH_ENDPOINT_URL>"
AZURE_SEARCH_ADMIN_KEY="<YOUR_AZURE_SEARCH_ADMIN_KEY>"
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
```

## Usage

1. Run the Streamlit application:
``` python
streamlit run streamlit.py
```
2. Open the application in your web browser.
3. Select a Microsoft Azure Certification and a project level.
4. Click the "Generate" button to generate a project idea.

## License

This project is licensed under the terms of the MIT license. See the LICENSE file for details.

## Author

- GitHub: [@rishabkumar7](https://github.com/rishabkumar7)
- Twitter: [@rishabincloud](https://x.com/rishabincloud)