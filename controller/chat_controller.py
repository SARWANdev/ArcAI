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
            new_conversation = self.conversation_service.create_conversation(user_id=user_id, document_ids=document_ids,
                                                                             project_ids=project_ids)
            new_conversation.add_user_message(user_prompt)

            self.conversation_service.update_name(new_conversation.conversation_id,
                                                  self.ai_service.generate_conversation_name(new_conversation))
            if not new_conversation.name:
                new_conversation.set_name(self.ai_service.generate_conversation_name(new_conversation))

            response = self.ai_service.send_chat_message(question=user_prompt, conversation=new_conversation)

            string_response = self.ai_service.output_streaming_response(response, len)
            new_conversation.add_ai_message(string_response)
            self.conversation_service.update_messages(new_conversation.conversation_id, new_conversation.get_messages())
            list_of_messages = new_conversation.get_messages()
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
            if old_conversation:
                old_conversation.add_user_message(user_prompt)
                response = self.ai_service.send_chat_message(question=user_prompt, conversation=old_conversation)

                string_response = self.ai_service.output_streaming_response(response, len)

                old_conversation.add_ai_message(string_response)

                self.conversation_service.update_messages(old_conversation.conversation_id, old_conversation.get_messages())

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

    def get_conversation_for_document(self):
        try:
            # Extract query parameters
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")[0]

            print(user_id, document_id)

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            conversation = self.conversation_service.get_conversation_by_document_id(document_id)
            conversation_id = conversation.conversation_id
            conversation_messages = conversation.get_messages()
            print(conversation_id)
            print(conversation_messages)

            return jsonify({
                "status": "success",
                "data": {
                    "conversation_id": str(conversation_id),
                    "list_of_messages": conversation_messages
                }
            }), 200


        except Exception as e:
            print(f"Error in get_conversation: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def get_chat_history(self, user_id):
        pass

    def get_conversation(self, chat_id):
        pass

    def delete_all_chats(self, user_id):
        """
        Deletes all chat sessions for a user.
        """
        return self.conversation_service.delete_all_chats(user_id)
    
    def get_user_conversations(self):
        try:
            # Get paramaeters from query string
            user_id = request.args.get("user_id")
            sort_by = request.args.get("sort_by", "CreatedAt")
            order = request.args.get("order", "desc")
            print(user_id, sort_by, order)

            # Map frontend field names to database columns
            if sort_by == "Title":
                sort_by = "name"
            elif sort_by == "CreatedAt":
                sort_by = "created"



            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            conversation_model_list = self.conversation_service.sort_history(user_id, sort_by, order)

            conversation_list = [
                {
                    "Title": model.name,
                    "CreatedAt": model.created_at,
                    "ConversationId": str(model.conversation_id)
                }
                for model in conversation_model_list
            ]
            return jsonify({
                "status": "success",
                "message": "History retrieved successfully",
                "data": {
                    "conversations": conversation_list,
                    "sort_by": sort_by,
                    "order": order
                }
            }), 200
        
        except Exception as e:
            print(f"Error in get_user_conversation: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to retrieve projects",
                "error": str(e)
            }), 500

    def get_conversation_from_conversation_id(self):
        try:
            # Extract query parameters
            data = request.get_json()
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")

            print(user_id, conversation_id)

            if not user_id or not conversation_id:
                return jsonify({"error": "Missing user_id or conversation_id"}), 400

            conversation = self.conversation_service.get_conversation(conversation_id)
            conversation_id = conversation.conversation_id
            conversation_messages = conversation.get_messages()

            return jsonify({
                "status": "success",
                "data": {
                    "conversation_id": str(conversation_id),
                    "list_of_messages": conversation_messages
                }
            }), 200


        except Exception as e:
            print(f"Error in get_conversation_from_conversation_id: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def delete_chat(self):
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")
            print(user_id, conversation_id)
            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.conversation_service.delete_chat(conversation_id)
            # Return both success message
            return jsonify({
                "status": "success",
                "message": "Conversation deleted successfully",
            }), 200

        except Exception as e:
            print(f"Error in delete_chat: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "Failed to delete the chat",
                "error": str(e)
            }), 500

    def rename_chat(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            conversation_id = data.get('conversation_id')
            new_name = data.get('name')
            print(user_id, conversation_id, new_name)

            if not all([user_id, conversation_id, new_name]):
                return jsonify({'error': 'Missing required fields'}), 400
            print("renaming")
            result = self.conversation_service.rename_chat(conversation_id, new_name)
            print("renamed")
            if result:
                return jsonify({
                    "status": "success",
                    "message": "Conversation renamed successfully"
                }), 200
            else:
                return jsonify({
                    "status": "error",
                    "message": "Failed to rename the conversation"
                }), 500
        except Exception as e:
            return jsonify({
                "status": "error", "message": str(e)
            }), 500

    def register_chat_routes(self, app):
        app.add_url_rule("/chat", view_func=self.query, methods=["POST"])
        app.add_url_rule("/chat/follow-up", view_func=self.follow_up, methods=["POST"])
        app.add_url_rule("/chat/history", view_func = self.get_user_conversations)
        app.add_url_rule("/chat/conversation/document", view_func=self.get_conversation_for_document, methods=["POST"])
        app.add_url_rule("/chat/conversation", view_func=self.get_conversation_from_conversation_id, methods=["POST"])
        app.add_url_rule("/chat/delete", view_func=self.delete_chat, methods=["DELETE"])
        app.add_url_rule("/chat/rename", view_func=self.rename_chat, methods=['PATCH'])
        app.register_blueprint(self.chat)
