
import os
import sys
import subprocess
import webbrowser
import asyncio

py_env = os.path.join(os.path.dirname(__file__), 'py-env-site-packages')
os.makedirs(py_env, exist_ok=True)
sys.path.append(py_env)

try:
  import aiohttp
except:
  subprocess.run([
    sys.executable, '-m', 'pip', 'install', f'--target={py_env}', 'aiohttp'
  ])
  import aiohttp

import aiohttp.web

async def websocket_handler(request):
  ws = aiohttp.web.WebSocketResponse()
  await ws.prepare(request)

  async for msg in ws:
    if msg.type == aiohttp.WSMsgType.TEXT:
        if msg.data == 'close':
            await ws.close()
        else:
            await ws.send_str(msg.data + '/answer')
    elif msg.type == aiohttp.WSMsgType.ERROR:
        print(f'ws connection closed with exception {ws.exception()}')

  print('websocket connection closed')

  return ws


async def hello(request):
  return aiohttp.web.Response(text="Hello, world")

async def on_server_startup(app):
  # Open a web browser to ourselves! We jump on another thread so the server can spin up _while_ we're in webbrowser.open() (which takes a quarter-second)
  loop = asyncio.get_event_loop()
  loop.create_task(
    asyncio.to_thread(
      lambda: webbrowser.open('http://127.0.0.1:8081')
    )
  )


def sync_main():
  server_app = aiohttp.web.Application()

  server_app.on_startup.append(on_server_startup)

  server_app.add_routes([
    aiohttp.web.get('/', hello),
    aiohttp.web.get('/ws', websocket_handler)
  ])

  aiohttp.web.run_app(
    server_app,
    host='127.0.0.1',
    port=8081
  )


if __name__ == '__main__':
  sync_main()
