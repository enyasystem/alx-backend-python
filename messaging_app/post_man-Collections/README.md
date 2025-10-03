Postman collection for Messaging App API

Usage

1. Import `Messaging App.postman_collection.json` into Postman.
2. Create an environment and set `base_url` to your server (e.g., http://127.0.0.1:8000).
3. Update `username` and `password` environment variables to valid credentials.
4. Run requests in this order (the collection scripts set tokens/ids automatically):
   - Obtain JWT Token (sets `access_token` env var)
   - Create Conversation (sets `conversation_id`)
   - Create Message
   - List Conversations
   - List Messages

Example responses

- Obtain token (200):

{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}

- Create Conversation (201):

{
  "conversation_id": "<uuid>",
  "participants": [ ... ],
  "created_at": "2025-10-03T..."
}

- Create Message (201):

{
  "message_id": "<uuid>",
  "sender": "<user_uuid>",
  "conversation": "<conversation_uuid>",
  "message_body": "Hello from Postman!",
  "sent_at": "2025-10-03T..."
}

- Unauthorized access (401 or 403):

{
  "detail": "Authentication credentials were not provided."  
}
