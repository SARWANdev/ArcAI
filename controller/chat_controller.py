from services.ai_service import AIService
from services.document_service import DocumentService
from services.ai_service import AIService
from model.ai_chat.conversation import Conversation
from flask import Blueprint, Flask, jsonify, request
from pathlib import Path
import os

class ChatController:
    def __init__(self, app : Flask):
        self.ai_service = AIService()
        self.chat = Blueprint('chat', __name__)
        self.document_service = DocumentService()
        self.ai_service = AIService()
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
            # The document id is required
            data = request.get_json()
            home_dir = os.path.expanduser("~")
            document_dir = os.path.join(home_dir, 'Documents')
            upload_folder_path = os.path.join(document_dir, "uploads")
            user_id = data.get("user_id")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            user_prompt = data.get("user_prompt")
            document_name = data.get("document_name")
            document_path = os.path.join(upload_folder_path, document_name)
            # 1st step : Getting text chunks using get_text_chunks
            text_chunks = self.document_service.get_text_chunks(document_path)
            # 2nd step : Get_vector_store in ai_service and use it on the text chunks
            vector_store = self.ai_service.get_vector_store(text_chunks)
            # 3rd step : Initialise conversation instance and give it embedding as an argument
            # and generate a random id
            self.new_conversation = Conversation(vector_store, user_id)
            # 4th step : Conversation Model has method to add user message
            self.new_conversation.add_user_message(user_prompt)
            # 5th step : Use send_chat_message and add the user question and conversation instance,
            # which will give response Object
            response = self.ai_service.send_chat_message(user_prompt, self.new_conversation)

            response_string = self.ai_service.output_streaming_response(response, len)
            print(response_string)


            # Call your service layer

            return jsonify({"success": "The prompt was sent successfully to the backend"}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    def summarize(self, document_id):
        pass

    def follow_up(self, chat_id, prompt):
        pass

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
        app.register_blueprint(self.chat)
