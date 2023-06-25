# chatgpt-retrieval

## Requirements

Python >3.10.12

## Installation

```
pip install -r requirements.txt
```

Put your OpenAI api key into `constants.py`.

Symlink for your project directory:

`ln -s ~/path/to/your-project project` 

Put any links to documentation that should be scraped and added into the urls.txt file (one url per line).

## usage

## basic usage, building new vector store every time

python chatgpt.py "Summarise what my web application does in 3 sentences."

## usage with saving vector store locally

python chatgpt.py "Summarise what my web application does in 3 sentences." --persist

## generate metadata

`generateMetadata.py` can be used to read project files and give it to gpt to generate a summary and tags for it.
