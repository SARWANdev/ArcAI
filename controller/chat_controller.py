from services.ai_service import AIService
from services.conversation_service import ConversationService
from services.ai_service import AIService
from flask import Blueprint, Flask, jsonify, request



class ChatController:
    """
    Controller class to handle chat-related HTTP requests, integrating with AI services and
    conversation management. Registers routes for querying, follow-ups, conversation history,
    conversation retrieval, deletion, renaming, clearing, and searching chats.

    Attributes:
        ai_service (AIService): Service for AI-related operations including generating conversation names and sending chat messages.
        conversation_service (ConversationService): Service managing conversation logic.
        chat (Blueprint): Flask Blueprint for chat routes.
    """

    def __init__(self, app: Flask):
        """
        Initializes the ChatController by creating service instances and registering routes.

        Args:
            app (Flask): The Flask application instance to which routes will be registered.
        """
        self.ai_service = AIService()
        self.conversation_service = ConversationService()
        self.chat = Blueprint('chat', __name__)
        self.register_chat_routes(app)

    def query(self):
        """
        Handles POST requests to initiate a new conversation based on user input and related document/project IDs.
        Creates a new conversation, adds the user prompt, generates AI response, updates conversation name and messages,
        and returns the updated conversation details.

        Returns:
            JSON response containing success status, conversation ID, and list of messages or error details.
        """
        try:
            # Get form fields
            data = request.get_json()
            user_id = data.get("user_id")
            user_prompt = data.get("user_prompt")
            document_ids = data.get("document_ids")
            project_ids = data.get("project_ids")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            new_conversation = self.conversation_service.create_conversation(
                user_id=user_id,
                document_ids=document_ids,
                project_ids=project_ids)
            new_conversation.add_user_message(user_prompt)

            self.conversation_service.update_name(
                new_conversation.conversation_id,
                self.ai_service.generate_conversation_name(new_conversation))
            if not new_conversation.name:
                new_conversation.set_name(self.ai_service.generate_conversation_name(new_conversation))

            response = self.ai_service.send_chat_message(question=user_prompt, conversation=new_conversation)

            string_response = self.ai_service.output_streaming_response(response, len)
            new_conversation.add_ai_message(string_response)
            self.conversation_service.update_messages(new_conversation.conversation_id, new_conversation.get_messages())
            list_of_messages = new_conversation.get_messages()

            return jsonify({
                "success": True,
                "data": {"conversation_id": str(new_conversation.conversation_id),
                         "list_of_messages": list_of_messages}
            }), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    def follow_up(self):
        """
        Handles POST requests for follow-up messages in an existing conversation.
        Retrieves the conversation, adds the new user message, sends it to the AI service,
        updates the conversation with the AI response, and returns the updated messages.

        Returns:
            JSON response containing success status, conversation ID, and list of messages or error details.
        """
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

                self.conversation_service.update_messages(old_conversation.conversation_id,
                                                          old_conversation.get_messages())

                list_of_messages = old_conversation.get_messages()

                return jsonify({
                    "success": True,
                    "data": {"conversation_id": str(old_conversation.conversation_id),
                             "list_of_messages": list_of_messages}
                }), 200

        except Exception as e:
            print(e)
            return jsonify({"error": str(e)}), 500

    def get_conversation_for_document(self):
        """
        Retrieves a conversation associated with a given document for a specific user.

        Expects a JSON body with 'user_id' and 'document_id' (list with at least one element).

        Returns:
            JSON response with the conversation ID and list of messages or error details.
        """
        try:
            # Extract query parameters
            data = request.get_json()
            user_id = data.get("user_id")
            document_id = data.get("document_id")

            if not user_id or not document_id:
                return jsonify({"error": "Missing user_id or document_id"}), 400

            conversation = self.conversation_service.get_conversation_by_document_id(document_id[0])
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
            return jsonify({"error": str(e)}), 500

    def delete_all_conversations(self, user_id):
        """
        Deletes all conversations associated with a given user.

        Args:
            user_id (str): The user identifier.

        Returns:
            The result of the deletion operation from the conversation service.
        """
        return self.conversation_service.delete_all_conversations(user_id)

    def get_user_conversations(self):
        """
        Retrieves a list of conversations for a user, with optional sorting by title or creation date.

        Query parameters:
            user_id (str): Required user identifier.
            sort_by (str): Optional; "Title" or "CreatedAt" (default).
            order (str): Optional; "asc" or "desc" (default "desc").

        Returns:
            JSON response containing the list of conversations, sorting info, or error details.
        """
        try:
            # Get parameters from query string
            user_id = request.args.get("user_id")
            sort_by = request.args.get("sort_by", "CreatedAt")
            order = request.args.get("order", "desc")

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
            return jsonify({"error": str(e)}), 500

    def get_conversation(self):
        """
        Retrieves a conversation by conversation ID for a given user.

        Expects a JSON body with 'user_id' and 'conversation_id'.

        Returns:
            JSON response containing the conversation ID and list of messages or error details.
        """
        try:
            # Extract query parameters
            data = request.get_json()
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")

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
            print(f"Error in get_conversation: {e}")
            return jsonify({"error": str(e)}), 500

    def delete_chat(self):
        """
        Deletes a single conversation given a conversation ID.

        Expects a JSON body with 'user_id' and 'conversation_id'.

        Returns:
            JSON response confirming deletion or error details.
        """
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            conversation_id = data.get("conversation_id")
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
            return jsonify({"error": str(e)}), 500

    def rename_chat(self):
        """
        Renames an existing conversation.

        Expects a JSON body with 'user_id', 'conversation_id', and new 'name'.

        Returns:
            JSON response confirming rename success or error details.
        """
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            conversation_id = data.get('conversation_id')
            new_name = data.get('name')

            if not all([user_id, conversation_id, new_name]):
                return jsonify({'error': 'Missing required fields'}), 400
            self.conversation_service.update_name(conversation_id, new_name)
            return jsonify({
                "status": "success",
                "message": "Conversation renamed successfully"
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def clear_history(self):
        """
        Deletes all conversations for a given user.

        Expects a JSON body with 'user_id'.

        Returns:
            JSON response confirming all conversations deleted or error details.
        """
        try:
            # Get parameters from query string
            data = request.get_json()
            user_id = data.get("user_id")
            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            self.conversation_service.clear_history(user_id)
            # Return both success message
            return jsonify({
                "status": "success",
                "message": "All conversations deleted successfully",
            }), 200

        except Exception as e:
            print(f"Error in delete_all: {str(e)}")
            return jsonify({"error": str(e)}), 500

    def search_chats(self):
        """
        Searches conversations for a user based on a query string.

        Query parameters:
            user_id (str): Required user identifier.
            query (str): Search query string.

        Returns:
            JSON response containing search results or error details.
        """
        try:
            # Get parameters from query string
            user_id = request.args.get("user_id")
            query = request.args.get("query")

            if not user_id:
                return jsonify({"error": "user_id is required"}), 400

            searches = self.conversation_service.search_conversations(user_id, query)

            chats = []
            for chat in searches:
                dictionary = {"Title": chat.name, "ConversationId": chat.conversation_id}
                chats.append(dictionary)

            return jsonify({
                "status": "success",
                "results": chats,
                "message": "Search retrieved successfully",
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def register_chat_routes(self, app):
        """
        Registers all chat-related routes on the Flask app.

        Args:
            app (Flask): The Flask application instance.
        """
        app.add_url_rule("/chat", view_func=self.query, methods=["POST"])
        app.add_url_rule("/chat/follow-up", view_func=self.follow_up, methods=["POST"])
        app.add_url_rule("/chat/history", view_func=self.get_user_conversations)
        app.add_url_rule("/chat/conversation/document", view_func=self.get_conversation_for_document, methods=["POST"])
        app.add_url_rule("/chat/conversation", view_func=self.get_conversation, methods=["POST"])
        app.add_url_rule("/chat/delete", view_func=self.delete_chat, methods=["DELETE"])
        app.add_url_rule("/chat/rename", view_func=self.rename_chat, methods=['PATCH'])
        app.add_url_rule("/chat/delete-all", view_func=self.clear_history, methods=['DELETE'])
        app.add_url_rule("/chat/search", view_func=self.search_chats)
        app.register_blueprint(self.chat)
