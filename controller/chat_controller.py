from datetime import datetime, timezone
from bson import ObjectId
from services.ai_service import AIService
from services.document_service import DocumentService
from services.ai_service import AIService
from model.ai_chat.conversation import Conversation
from flask import Blueprint, Flask, jsonify, request
from database.repository.conversation_repository import ConversationRepository
from pathlib import Path
import os

class ChatController:
    def __init__(self, app : Flask):
        self.ai_service = AIService()
        self.chat = Blueprint('chat', __name__)
        self.document_service = DocumentService()
        self.ai_service = AIService()
        self.conversation_repository = ConversationRepository
        self.new_conversation = None
        # 1st step : Getting text chunks using get_text_chunks
        # 2nd step : Get_vector_store in ai_service and use it on the text chunks
        # 3rd step : Initialise conversation instance and give it embedding as an argument and generate a random id
        # 4th step : Get question from the user in frontend and send it to backend#
        # 5th step : Conversation Model has method to add user message
        # 6th step : Use send_chat_message and add the user question and conversation instance, which will give response Object
        # 7th step : Use ai_service.output_streaming_response method to stream the response
        # 8th step : The string output wil be added to Conversation model (add_ai_message)


        # 1st step
        self.register_chat_routes(app)

    def query(self):
        try:
            # Get form fields
            user_id = request.form.get("user_id")
            user_prompt = request.form.get("user_prompt")
            document_name = request.form.get("document_name")
            uploaded_file = request.files.get("file")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400
            if not uploaded_file or not document_name:
                return jsonify({"error": "file and document_name are required"}), 400


            # 1st step : Getting text chunks using get_text_chunks
            text_chunks = self.document_service.get_text_chunks(uploaded_file)

            # 2nd step : Get vector store
            vector_store = self.ai_service.get_vector_store(text_chunks)

            conversation_id = str(ObjectId())
            # 3rd step : Initialise conversation
            self.new_conversation = Conversation(vector_store=vector_store, user_id=user_id, conversation_id=str(ObjectId()), name = "Conversation 1",
                                                 created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))

            # Creating the list to save the conversation


            # 4th step : Add user message
            self.new_conversation.add_user_message(user_prompt)

            # 5th step : Get response
            response = self.ai_service.send_chat_message(user_prompt, self.new_conversation)

            # 6th step : Use ai_service.output_streaming_response method to stream the response
            response_string = self.ai_service.output_streaming_response(response, len)
            # This will give me list of messages between user an AI
            # Unique conversation id to access the conversation everytime
            list_of_messages = self.new_conversation.get_messages()
            self.new_conversation.add_ai_message(response_string)

            return jsonify({
                "success": True,
                "data": {"list_of_messages" : list_of_messages, "conversation_id": conversation_id}
            }), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    def summarize(self, document_id):
        pass

    def follow_up(self):
        try:
            data = request.get_json()
            user_id = data.get("user_id")
            user_prompt = data.get("user_prompt")
            conversation_id = data.get("conversation_id")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            print(f"The user {user_id} with the user prompt {user_prompt} wants answer with conversation id : {conversation_id}")

            return jsonify({
                "success": True,
                "data": "The follow up has been a success"
            }), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500


    def get_chat_history(self, user_id):
        pass

    def get_conversation(self, chat_id):
        pass

    def rename_chat(self, chat_id, new_title):
        """
        Renames an existing chat session.
        """
        return self.ai_service.rename_chat(chat_id, new_title)

    def delete_chat(self, chat_id):
        """
        Deletes a chat session and its messages.
        """
        return self.ai_service.delete_chat(chat_id)
    
    def delete_all_chats(self, user_id):
        """
        Deletes all chat sessions for a user.
        """
        return self.ai_service.delete_all_chats(user_id)

    def register_chat_routes(self, app):
        app.add_url_rule("/chat", view_func=self.query, methods=["POST"])
        app.add_url_rule("/chat/follow-up", view_func=self.follow_up, methods=["POST"])
        app.register_blueprint(self.chat)
