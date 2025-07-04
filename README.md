
# 🐍 Python Generators & Database Seeding 🚀

This project demonstrates advanced usage of Python generators for efficient data processing and seamless integration with MySQL databases.

## 📦 Features
- Stream data from SQL databases using Python generators
- Batch process large datasets without overloading memory
- Simulate real-world scenarios with live data updates
- Perform memory-efficient aggregate calculations
- Integrate Python with MySQL for robust data management

## 🗄️ Database Schema
The main table used for seeding is:

| Column   | Type         | Description                |
|----------|--------------|----------------------------|
| user_id  | UUID (PK)    | Unique user identifier     |
| name     | VARCHAR      | User's name (not null)     |
| email    | VARCHAR      | User's email (not null)    |
| age      | DECIMAL      | User's age (not null)      |

## 🚦 Quick Start
1. Clone the repo and navigate to the project directory.
2. Install dependencies:
   ```sh
   pip install mysql-connector-python
   ```
3. Update your MySQL credentials in `seed.py` if needed.
4. Run the seeding script:
   ```sh
   python seed.py
   ```

## 📂 Project Structure
| File         | Purpose                                      |
|--------------|----------------------------------------------|
| seed.py      | Main script for DB connection and seeding    |
| README.md    | Project documentation                        |
| user_data.csv| Sample data for seeding (if provided)        |

## 🎯 Learning Objectives
- Master Python generators for iterative data processing
- Handle large datasets efficiently
- Simulate live data and streaming scenarios
- Optimize performance with batch and lazy loading
- Integrate Python with SQL for real-world applications

## 📚 Resources
- [Python Generators](https://realpython.com/introduction-to-python-generators/)
- [MySQL Connector/Python Docs](https://dev.mysql.com/doc/connector-python/en/)
