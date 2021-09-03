FIRST STEPS AFTER CLONE REPOSITORY

1. Please complete the "env" file then rename it to ".env"

    DATABASE=database_name
    DB_USER=database_user
    HOST=database_host
    PASSWORD=user_password
    PORT=database_port
    SECRET_KEY=random_generated_key

    *For example the key could be the output of:
        python3 -c 'import os; print(os.urandom(16))'

2. After populating ".env" file, create a virtual environment and activate it:

    python3 -m venv venv
    source venv/bin/activate

3. Install dependences

    pip install -r requirements.txt

4. Launch application

    python3 app.py


