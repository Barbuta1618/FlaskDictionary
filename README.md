FIRST STEPS AFTER CLONE REPOSITORY

1. Create ".env" file having this structure:

    DATABASE=database_name
    DB_USER=database_user
    HOST=database_host
    PASSWORD=user_password
    PORT=database_port

2. After populating ".env" file, create a virtual environment and activate it:

    python3 -m venv venv
    source venv/bin/activate

3. Install dependences

    pip install -r requirements.txt

4. Launch application

    python3 app.py


