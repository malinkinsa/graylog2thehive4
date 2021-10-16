import uvicorn
import argparse

arg = argparse.ArgumentParser()
arg.add_argument('--url', required=True)
arg.add_argument('--api_key', required=True)
arg.add_argument('--ip', required=True)
arg.add_argument('--port', default=8000)

args = vars(arg.parse_args())
url = args['url']
api_key = args['api_key']
ip = args['ip']
port = args['port']


if __name__ == "__main__":
    uvicorn.run("app.webhook:webhook", host=ip, port=port, reload=True)
