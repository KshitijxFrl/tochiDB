import argparse
import os
import json
from dotenv import load_dotenv
from http.server import HTTPServer

from .tochiServerSetup import RequestHandeler
from .envWright import EnvWriter

from .pgdbConnector import inititalize_connection_pool, shutdown_connection_pool
from .utility import tochilogo, load_query_cache, update_close_query_cache, initialize_norConverter


def runserver():
    load_dotenv("./.env")

    host  = os.getenv("HOST")
    port  = int(os.getenv("PORT"))

    db_settings = {
        "DB_NAME":os.getenv("DB_NAME"), 
        "DB_HOST":os.getenv("DB_HOST"), 
        "DB_PORT":os.getenv("DB_PORT"),
        "DB_PASSWORD":os.getenv("DB_PASSWORD"),
        "AD_USERNAME":os.getenv("AD_USERNAME")
    }     

    
    server = HTTPServer((host, port), RequestHandeler)

    try:
        tochilogo()
        print (f"Starting the tochi server at host: {host} and port: {port} [ctrl + c to shutdown the server].....")
        inititalize_connection_pool(dbsettings=db_settings)
        initialize_norConverter()
        load_query_cache()
        server.serve_forever()
    except KeyboardInterrupt:
        print("Server is shutting down....")
        server.server_close
        shutdown_connection_pool()
        update_close_query_cache()    
    finally:
        print("Shutting down completed.....")


def listenTDB(natural_quary):
    load_dotenv("./.env")

    host  = os.getenv("HOST")
    port  = os.getenv("PORT")

    print(f'{host}  {port}')



def intialization():
    print("Tochi has started in the selceted folder...!!")

    tochi_config = ".env"

    if os.path.exists(tochi_config):
        overwite = input("Do you want to overwrite the initialization [y / n].")
        if overwite != 'y':
            print("intitalization aboarded....!!")
            return


    DB_DETAILS = {
        "HOST": input("Enter database host (default: localhost): ") or "127.0.0.1",
        "PORT": input("Enter database port (default: 5432): ") or 5432,
        "DATABASE": input("Enter database name: ") or "tochi_db",
        "USERNAME": input("Enter username: ") or "postgres",
        "PASSWORD": input("Enter password: "),
        "API_KEY": input("Enter your ai key: ")
    }

    try:
        EnvWriter.write_env('.env', DB_DETAILS, mode='overwrite')  
        with open("./cache.json", "x") as file:
            json.dump({"query_cache": {}}, file)
    except Exception as e:
        print(f"Troble initalizing the tochi in the current directory..!! Exiting with error {e}.")        
            


#! The main cli function
def main():
    parser = argparse.ArgumentParser(description = "Welcome to tochiDB !!")
    subparsers = parser.add_subparsers(dest="command", help="tochiDB user command")
    
    subparsers.add_parser("init", help="Intialize tochi in the selected folder/directory")

    listen = subparsers.add_parser("listen", help="Send your request to tochi")
    #! nargs="+" help us to collect everything after tochi listen
    listen.add_argument("nql", nargs="+" , help="Natural query for tochi")


    subparsers.add_parser("runserver", help="Start the tochi server.")

    args = parser.parse_args()

    if args.command == "init":
        intialization()
    elif args.command =="listen":

        naturalquery = " ".join(args.nql)
        listenTDB(naturalquery)    

    elif args.command == "runserver":
        runserver()

if __name__ == "__main__":
    main()