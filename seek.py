import os
import sys
import requests
import openai
import glob
import constants
from bs4 import BeautifulSoup
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader, UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import Chroma

def scrape_webpages(urls):
    scraped_data = []
    print("Scraping data and storing urls: ", urls)
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        scraped_data.append(text)
    return scraped_data

def store_scraped_data(scraped_data):
    for i, text in enumerate(scraped_data):
        with open(f'web_content/page{i}.txt', 'w') as f:
            f.write(text)
    print("Stored data in web_content folder")

def get_index(PERSIST):
    if PERSIST and os.path.exists("persist"):
        print("Reusing index...\n")
        vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
        from langchain.indexes.vectorstore import VectorStoreIndexWrapper
        return VectorStoreIndexWrapper(vectorstore=vectorstore)
    else:
        print("Loading all files into loaders...\n")
        return create_index_from_loaders(PERSIST)

def create_index_from_loaders(PERSIST):
    dir_path = 'project/'
    file_types = ['html', 'js', 'json', 'txt', 'md', 'toml']
    loaders = []
    for file_type in file_types:
        glob_pattern = '**/*.' + file_type
        for file_path in glob.glob(os.path.join(dir_path, glob_pattern), recursive=True):
            # Exclude files in "node_modules"
            if "node_modules" not in file_path:
                if file_type == 'html':
                    print("Loading", file_path, "as unstructured HTML")
                    loader = UnstructuredHTMLLoader(file_path)
                else:
                    print("Loading", file_path, "as text")
                    loader = TextLoader(file_path)
                loaders.append(loader)

    web_content_loader = DirectoryLoader('web_content/', glob='**/*.txt',
                                        show_progress=True, use_multithreading=True,
                                        loader_cls=TextLoader)
    loaders.append(web_content_loader)

    total_docs = sum(len(loader.load()) for loader in loaders)
    print("Finished loading all files into loaders\n")
    print("Loaded", total_docs, "documents\n")

    if PERSIST:
        return VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders(loaders)
    else:
        return VectorstoreIndexCreator().from_loaders(loaders)

def create_chain(index):
    modelName =  sys.argv[sys.argv.index('-m') + 1] if '-m' in sys.argv else "gpt-3.5-turbo"
    print("Creating chain with model:", modelName, "\n")
    return RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model=modelName),
        retriever=index.vectorstore.as_retriever(search_kwargs={"k": 10}),
    )

if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = constants.APIKEY
    query = sys.argv[sys.argv.index('-q') + 1] if '-q' in sys.argv else sys.exit("No query provided")
    PERSIST = sys.argv.index('--persist') if '--persist' in sys.argv else False

    urls = []
    with open('urls.txt', 'r') as f:
        for line in f:
            urls.append(line.strip())
    scraped_data = scrape_webpages(urls)
    store_scraped_data(scraped_data)
    
    index = get_index(PERSIST)
    chain = create_chain(index)
    
    print("Running query:", query, "\n")
    print(chain.run(query))