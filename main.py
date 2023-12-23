import sqlalchemy
print(sqlalchemy.__version__)
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import click



@click.command()
@click.option('--query', '-q', required='True')
def retrieve(query):
    
    loader = TextLoader('data.txt')
    index = VectorstoreIndexCreator().from_loaders([loader])
    chain = ConversationalRetrievalChain.from_llm(
        llm=ChatOpenAI(model='gpt-3.5-turbo'),
        retriever=index.vectorstore.as_retriever(
            search_kwargs={'k': 1} # найбільш релевантний answer
        )
    )
    chat_log = []
    result = chain({'question': query, 'chat_history': chat_log})
    click.echo(result['answer'])

    chat_log.append((query, result['answer']))


if __name__ == '__main__':
    retrieve()
# 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