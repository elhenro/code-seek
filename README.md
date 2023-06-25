# code-seek

> Give GPT detailed knowledge about your project and add information from the web.

Simple python script to scrape web and local content, store it, then use it to answer queries. Initially, it reads a list of URLs from a file, scrapes the web content from these URLs, and stores text. Then, it creates an index from the stored data and other files in the project directory, and uses this index to power a question-answering system based on OpenAI's language models, to answer questions based on the indexed data.

## Requirements

- Python version 3.10.12 or higher

## Installation

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

2. Add your OpenAI API key to constants.py.

3. Create a symbolic to your project directory:

`ln -s ~/path/to/your-project project` 

4. Add any URLs for documentation that should be scraped to the urls.txt file (one URL per line).

## usage

### basic usage

This command builds a new vector store each time it's run:

```bash
python seek.py -q "Summarise what my web application does in 3 sentences."
```

## Usage with persistent vector store

This command saves the vector store locally for faster subsequent queries:

```bash
python seek.py -q "Summarise what my web application does in 3 sentences." --persist
```

## Size of vector store

```bash
du -sh store
```

## Additional Tools

The generateMetadata.py script can be used to read project files and generate a summary and tags for them using GPT.

- `generateMetadata.py`


# Docker

## Build

```bash
docker build -t code-seek .
```

## Run

```bash
docker run -it --rm code-seek "Summarise what my web application does in 3 sentences."
```