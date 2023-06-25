# code-seek

> Give GPT knowledge about your project and add any info from the web.

It is acomplished with the [retrieval plugin](https://github.com/openai/chatgpt-retrieval-plugin), which allows models to perform semantic searches against a vector database ([chroma](https://github.com/chroma-core/chroma)).

The `seek.py` script will scrape web and local content, store it in a vector db, then use it with openai models to answer queries.

Initially, it reads a list of URLs from a file, scrapes the web content from these URLs, and stores text. Then, it creates an index from the stored data and other files in the project directory, and uses this index to power a question-answering system, to answer questions based on the indexed data.

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

## Check size of vector store

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