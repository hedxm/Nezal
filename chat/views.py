from rest_framework.response import Response
from rest_framework.views import APIView
from .pusher import pusher_client
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain import hub
from langchain_community.tools import YouTubeSearchTool
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
# Create your views here.

class MessageAPIView(APIView):
    
    def get(self, request):
        # Extracting data from the request
        username = request.data.get('username')
        message = request.data.get('message')

        # Triggering the 'message' event on the 'chat' channel
        pusher_client.trigger('chat', 'message', {
            'username': username,
            'message': message,
        })
        
        # Responding with an empty response
        return Response({})
        
    # def post(self, request):
    #     messageReceived = request.data.get('message')
        
    #     messages = [
    #         {'username': 'Gepeto', 'message': "Soy Gepeto"},
    #         {'username': 'Usuario', 'message': messageReceived},
    #     ]
        
    #     return Response(messages)
    def post(self, request):
        # Buscar la forma de pasar el mensaje recibido a string
        messageReceived = request.data.get('message')
        messageReceivedStr = str(messageReceived)
        
        messages = [
            {'username': 'Gepeto', 'message': "Soy Gepeto"},
            {'username': 'Usuario', 'message': "Recibido: "+messageReceivedStr},
        ]
        
        llm = ChatOpenAI(openai_api_key="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",
                            temperature=0)

        graph = Neo4jGraph(
            url="neo4j+s://396a6556.databases.neo4j.io",
            username="neo4j",
            password="z9KsfP5HKYYn_KfST7EGt59QuibQqg-uOuxql7Rqjd0",
        )

        CYPHER_TEMPLATE = """
        You are an expert Neo4j Developer translating user questions into Cypher to answer questions about 
        songs' artist, genre of a song and the lyrics of songs.
        Convert the user's question based on the schema.

        Instructions:
        Use only the provided relationship types and properties in the schema.
        Do not use any other relationship types or properties that are not provided.

        If no data is returned, do not attempt to answer the question.

        Examples:

        To find the lyrics of a song or title:
        MATCH (t:Title)
        WHERE t.titleId = "Despacito"
        RETURN t.lyrics

        Schema: {schema}
        Question: {question}
        """

        cypher_generation_prompt = PromptTemplate(
            template=CYPHER_TEMPLATE,
            input_variables=["schema", "question"],
        )

        cypher_chain =  GraphCypherQAChain.from_llm(
            llm,
            graph=graph,
            cypher_prompt=cypher_generation_prompt,
            verbose=True
        )

        prompt = PromptTemplate(
            template="""
            You are a music expert. You can answer questions about songs and generate 
            lyrics, haikus or poems based in 
            the style of the artist, genre or song that the user indicates.

            Chat History:{chat_history}
            Question:{input}
            """,
            input_variables=["chat_history", "input"],
        )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        chat_chain = LLMChain(llm=llm, prompt=prompt, memory=memory)

        youtube = YouTubeSearchTool()

        tools = [
            Tool.from_function(
                name="Music info Chat",
                description="For when you need to chat about specific music artist or especific lyric of a song."
                            +"The question will include the words 'which' or 'what' at the beginning and 'lyrics' on the middle or at the end."
                            +"if the question includes the word or 'named', 'name' or 'song' changed for 'title'."
                            +"The question will be a string. Return a string.",
                func=cypher_chain.run,
                return_direct=True,
            ),
            Tool.from_function(
                name="Music Chat",
                description="For when you need to chat about music, lyrics or poems."
                            +"The question will be a string. Return a string.",
                func=chat_chain.run,
                return_direct=True
            ),
            Tool.from_function(
                name="Musics Video Search",
                description="Use when needing to find a music video. The question will include the word 'video'."
                            +"Return just one link to a YouTube video.",
                func=youtube.run,
                return_direct=True,
            ),
        ]

        agent_prompt = hub.pull("hwchase17/react-chat")
        agent = create_react_agent(llm, tools, agent_prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            memory=memory,
            max_interations=3,
            verbose=True,
            handle_parse_errors=True
        )
        
        response = agent_executor.invoke({"input":messageReceivedStr})
        #print(response["output"])
        return Response(response["output"])


