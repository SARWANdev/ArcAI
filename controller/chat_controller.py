from datetime import datetime, timezone
from bson import ObjectId
from services.ai_service import AIService
from services.conversation_service import ConversationService
from services.document_service import DocumentService
from services.ai_service import AIService
from model.ai_chat.conversation import Conversation
from flask import Blueprint, Flask, jsonify, request
from database.repository.conversation_repository import ConversationRepository
from pathlib import Path
import os


class ChatController:
    def __init__(self, app: Flask):
        self.ai_service = AIService()
        self.chat = Blueprint('chat', __name__)
        self.document_service = DocumentService()
        self.ai_service = AIService()
        self.conversation_repository = ConversationRepository
        self.conversation_service = ConversationService()
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
            data = request.get_json()
            user_id = data.get("user_id")
            user_prompt = data.get("user_prompt")
            document_ids = data.get("document_ids")
            project_ids = data.get("project_ids")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400
            print(1)
            new_conversation = self.conversation_service.create_conversation(user_id=user_id, document_ids=document_ids,
                                                                             project_ids=project_ids)
            print(2)
            new_conversation.add_user_message(user_prompt)
            print(3)
            self.conversation_service.rename_chat(new_conversation.conversation_id,
                                                  self.ai_service.generate_conversation_name(new_conversation))
            new_conversation.set_name(self.ai_service.generate_conversation_name(new_conversation))
            print(4)
            response = self.ai_service.send_chat_message(question=user_prompt, conversation=new_conversation)
            print(5)
            string_response = self.ai_service.output_streaming_response(response, len)
            print(6)
            new_conversation.add_ai_message(string_response)
            print(7)
            self.conversation_service.update_messages(new_conversation.conversation_id, new_conversation.get_messages())
            print(9)
            list_of_messages = new_conversation.get_messages()
            print(10)
            print(new_conversation.conversation_id)
            print(new_conversation.name)
            return jsonify({
                "success": True,
                "data": {"conversation_id": str(new_conversation.conversation_id),
                         "list_of_messages": list_of_messages}
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

            old_conversation = self.conversation_service.get_conversation(conversation_id)
            old_conversation.add_user_message(user_prompt)
            response = self.ai_service.send_chat_message(question=user_prompt, conversation=old_conversation)
            print(21)
            string_response = self.ai_service.output_streaming_response(response, len)
            print(22)
            old_conversation.add_ai_message(string_response)
            print(23)
            self.conversation_service.update_messages(old_conversation.conversation_id, old_conversation.get_messages())
            print(24)
            list_of_messages = old_conversation.get_messages()
            print(list_of_messages)
            return jsonify({
                "success": True,
                "data": {"conversation_id": str(old_conversation.conversation_id),
                         "list_of_messages": list_of_messages}
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