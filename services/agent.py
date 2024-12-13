# agent.py

import json
from langchain import hub
from langchain.agents import AgentExecutor, create_json_chat_agent
from langchain_community.agent_toolkits.load_tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional
import inflect
import re

from services.tool import book_meeting

load_dotenv()

class UserData(BaseModel):
    name: str
    email: str
    company: str
    description: Optional[str] = ""

class Agent:
    """
    A chat agent class responsible for handling and processing chat messages to generate
    responses using a language model and additional tools.

    This class initializes with a system prompt to define the agent's personality or context,
    loads necessary tools for enhancing responses (like web search capabilities), and sets up
    a language model for generating chat responses.

    Attributes:
        system_prompt (str): A prompt that defines the initial context or personality of the agent.
        agent_executor (AgentExecutor): An executor to manage the agent's response generation process,
                                        including interaction with tools and language models.

    Methods:
        add_prosody_to_utterance(utterance: str, prosody: dict) -> str:
            Enhances an utterance with prosody information.

        parse_hume_message(messages_payload: dict) -> tuple[str, list]:
            Parses incoming messages and extracts necessary information for response generation.

        get_response(message: str, chat_history: list = None) -> str:
            Generates a response based on the given message and chat history.

        number_to_words(number: str) -> str:
            Converts numerical strings within the response to their word equivalents.
    """

    def __init__(self, *, system_prompt: str, user_data: UserData):
        """
        Initializes the agent with a given system prompt and sets up necessary components for
        response generation, including tools and a language model.

        Args:
            system_prompt (str): A string that sets the initial context or personality of the agent.
        """
        
        self.system_prompt = system_prompt.format(
            name=user_data["name"], 
            email=user_data["email"], 
            company=user_data["company"], 
            description=user_data["description"]
        )

        meeting_tool = Tool(
            func=book_meeting,
            name="book_meeting",
            description="Schedule meeting by taking email for AgnetProd Demo"
        )

        tools = [meeting_tool]

        prompt = hub.pull("hwchase17/react-chat-json")

        llm = AzureChatOpenAI(deployment_name="gpt-4o")

        agent = create_json_chat_agent(llm, tools, prompt)

        self.agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )

    def add_prosody_to_utterance(self, utterance: str, prosody: dict) -> str:
        """
        Enhances an utterance by appending prosody information derived from prosody analysis.

        Args:
            utterance (str): The original text utterance to be enhanced.
            prosody (dict): A dictionary containing prosody features and their values.

        Returns:
            str: The enhanced utterance with prosody information appended.
        """

        prosody_string = ", ".join(prosody.keys())
        return f"Speech: {utterance} {prosody_string}"

    def parse_hume_message(self, messages_payload: dict):
        """
        Parses the payload of messages received from a client, extracting the latest user message
        and constructing the chat history with contextualized utterances.

        Args:
            messages_payload (dict): The payload containing messages from the chat.

        Returns:
            tuple[str, list]: A tuple containing the last user message and the constructed chat history.
        """

        messages = messages_payload["messages"]
        last_user_message = messages[-1]["message"]["content"]

        chat_history = [SystemMessage(content=self.system_prompt)]

        for message in messages[:-1]:

            message_object = message["message"]

            prosody_scores = message.get("models", {}).get("prosody", {}).get("scores", {})

            sorted_entries = sorted(
                prosody_scores.items(), key=lambda x: x[1], reverse=True
            )

            top_entries = sorted_entries[:3]

            top_entries_dict = {entry[0]: entry[1] for entry in top_entries}

            contextualized_utterance = self.add_prosody_to_utterance(
                message_object["content"], top_entries_dict
            )

            if message_object["role"] == "user":
                chat_history.append(HumanMessage(content=contextualized_utterance))
            elif message_object["role"] == "assistant":
                chat_history.append(AIMessage(content=contextualized_utterance))

        return [last_user_message, chat_history]

    def get_responses(self, message: str, chat_history=None) -> list[str]:
        """
        Generates responses to the user's message based on the current chat history and the
        capabilities of the integrated language model and tools.

        Args:
            message (str): The latest message from the user.
            chat_history (list, optional): The chat history up to this point. Defaults to None.

        Returns:
            list[str]: The stream of generated responses from the agent.
        """

        if chat_history is None:
            chat_history = []

        response = self.agent_executor.invoke(
            {
                "input": message,
                "chat_history": chat_history,
            }
        )
        output = response["output"]
        responses = []

        numbers = re.findall(r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b", output)
        for number in numbers:
            words = self.number_to_words(number)
            output = output.replace(number, words, 1)

        responses.append(json.dumps({"type": "assistant_input", "text": output}))
        responses.append(json.dumps({"type": "assistant_end"}))

        return responses

    def number_to_words(self, number):
        """
        Converts a number in string format into its word representation. For example,
        it would convert "42" to "forty-two". Useful for making numerical
        data more readable in responses.

        Args:
            number (str): The number to convert, in string format.

        Returns:
            str: The word representation of the given number.
        """
        p = inflect.engine()
        words = p.number_to_words(number)
        return words