from dotenv import dotenv_values

config = dotenv_values(".env")

database_url = config["DATABASE_URL"]
jwt_secret_key = config["JWT_SECRET_KEY"]
secret_key = config["SECRET_KEY"]
