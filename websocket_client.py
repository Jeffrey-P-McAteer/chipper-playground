
import os
import sys
import subprocess
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


try:
  import cmd2
except:
  subprocess.run([
    sys.executable, '-m', 'pip', 'install', f'--target={py_env}', 'cmd2'
  ])
  import cmd2

class HttpClientCliApp(cmd2.Cmd):
  def __init__(self, *args, **kwargs):
    super(HttpClientCliApp, self).__init__(*args, **kwargs)
    self.prompt = '> '

  def do_get(self, s: cmd2.Statement):
    self.poutput(f'Got s.arg_list = {s.arg_list}')

  def do_post(self, s: cmd2.Statement):
    self.poutput(f'Got s.arg_list = {s.arg_list}')

def main(args=sys.argv):
  print('Usage: ')
  print('  get http://server.com/path?params=123')
  print('  post http://server.com/path')
  print('    # Interactive prompt to paste in POST-ed data payload')
  print()
  print('Usage: ')
  c = HttpClientCliApp()
  sys.exit(c.cmdloop())


if __name__ == '__main__':
  main()
