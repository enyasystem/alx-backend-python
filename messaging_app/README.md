# 💬 Messaging App Backend

Welcome to the Messaging App backend project! This Django REST Framework project provides APIs for managing users, conversations, and messages in a chat application.

## 🚀 Features
- Custom user model with roles and phone number
- Create and list conversations with multiple participants
- Send and retrieve messages within conversations
- Nested API endpoints for easy access to related data
- Search and filter conversations and messages

## 🛠️ Tech Stack
- Python 3.x 🐍
- Django 5.x 🌐
- Django REST Framework 🛡️
- SQLite (default, easy to switch to PostgreSQL/MySQL)

## 📦 How to Run
1. Clone the repo
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Start the server: `python manage.py runserver`
5. Access the API at `http://localhost:8000/api/`

## 🧑‍💻 API Endpoints
- `/api/conversations/` : List, create, and manage conversations
- `/api/messages/` : List, create, and manage messages
- `/api-auth/` : Login/logout for browsable API

## 📝 Example Usage
- Create a conversation with participants
- Send a message to a conversation
- Retrieve all messages in a conversation

## 📚 Learning Outcomes
- Understand Django custom user models
- Build RESTful APIs with nested relationships
- Use serializers, viewsets, and routers in DRF

## 🤝 Contributing
PRs are welcome! Please open an issue or discussion for major changes.

Happy coding! 🚀
