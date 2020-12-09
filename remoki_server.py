#!/usr/bin/env python

import websockets
import asyncio
import importlib
from pynput.keyboard import Key
from pynput.keyboard import Controller as KBController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
# from key_mapping import special_key_mapping


# def reload_key_mapping():


async def forward_key_events(websocket, path):
  from key_mapping import special_key_mapping
  await websocket.send('server started')
  # reload_key_mapping()

  while True:
    try:
      msg = await websocket.recv()
      print(msg, '\t', websocket.remote_address[0])

      try:
        event, keycode = msg.split(' ')
      except ValueError:
        continue
      
      keycode_number = int(keycode)
      if not keycode_number in special_key_mapping.keys():
        key = chr(keycode_number)
      else:
        key = special_key_mapping[keycode_number]
      reply = f'> {msg}'


      if 'mouse' in event:
        clip = lambda x, lower, upper: min(upper, max(lower, x))
        clip(keycode_number, 0, 2)
        button = {
          0 : Button.left,
          1 : Button.middle,
          2 : Button.right
        }

        if 0 <= keycode_number <= 2:
          if event == 'mousedown':
            mouse.press(button[keycode_number])
          if event == 'mouseup':
            mouse.release(button[keycode_number])

      # left/right
      # if (event.location == 1) console.log('left ctrl');
      # if (event.location == 2) console.log('right ctrl');
      if event == 'keydown':
        keyboard.press(key)
          # keyboard.touch(key, True)
      if event == 'keyup':
        keyboard.release(key)
        if key == 'R':
          # reload key mapping
          import key_mapping
          importlib.reload(key_mapping)
          from key_mapping import special_key_mapping
          print('reload key_mapping')
          # reload_key_mapping()
        # import ipdb; ipdb.set_trace()

      await websocket.send(reply)

    except websockets.exceptions.ConnectionClosedOK:
      print('connection closed')
      break

keyboard = KBController()
mouse = MouseController()
start_server = websockets.serve(forward_key_events, '192.168.178.58', 8001, ping_interval=None)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

'''
from pynput.keyboard import Key, Controller
sleep(3)
keyboard.press(Key.left)
sleep(3)
keyboard.release(Key.left)

sleep(3)
keyboard.press('v')
sleep(3)
keyboard.release('v')

keyboard = Controller()

# Press and release space
keyboard.press(Key.space)
keyboard.release(Key.space)

# Type a lower case A; this will work even if no key on the
# physical keyboard is labelled 'A'
sleep(3)
keyboard.press('a')
sleep(3)
keyboard.release('a')

# Type two upper case As
keyboard.press('A')
keyboard.release('A')
with keyboard.pressed(Key.shift):
    keyboard.press('a')
    keyboard.release('a')

# Type 'Hello World' using the shortcut type method
keyboard.type('Hello World')
'''