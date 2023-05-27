from pydantic import BaseSettings

class Settings(BaseSettings): 
    database_password: str   #you dont have to give it a value. you can just stop at the str
    database_hostname: str
    database_name: str
    database_port: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


    class Config:  #this will import the env
        env_file= '.env'


settings = Settings()