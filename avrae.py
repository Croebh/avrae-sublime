
import sublime, sublime_plugin
import json
import os
import requests
import time
from functools import lru_cache

headers = {
            'Authorization': "",
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
          }


class gvarUpdateCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    file_name  = self.view.file_name()
    name       = self.view.name()
    getStatus  = 0
    postStatus = 0
    gvar       = None
    payload    = self.view.substr(sublime.Region(0, self.view.size()))

    if len(payload) > 100000:
      self.view.show_popup(
        '''<b>Error: Gvars must be less than 100k characters.'''.format(gvar), max_width=400)
    else:
      if name and name.endswith('.gvar'):
        if name.endswith('.gvar'):
          gvar = name[:36]
      elif file_name:
          gvar = os.path.basename(file_name)
          if gvar and gvar.endswith('.gvar'):
              gvar = gvar[:36]

      if gvar and len(gvar)==36:
        get, getStatus = avraeREST("GET", "customizations/gvars/" + gvar, ttl_hash=get_ttl_hash(5))
        newPayload = get.json()
        newPayload.update({"value":payload})
        post, postStatus = avraeREST("POST", "customizations/gvars/" + gvar, json.dumps(newPayload), ttl_hash=get_ttl_hash(5))
        if postStatus in (200, 201):
          self.window.active_view().show_popup(
            '''<b>Successfully Updated Gvar:</b>
            <ul>
              <li>
                <b>ID:</b> {}
              </li>
            </ul>'''.format(gvar), max_width=400)
      else:
        self.view.show_popup("<b>Something went wrong</b><br>Invalid Gvar ID - " + str(gvar), max_width=500)


class gvarGetCommand(sublime_plugin.WindowCommand):

  def run(self):
    name = self.window.active_view().name()
    self.file_name = self.window.active_view().file_name()
    self.view = self.window.active_view()
    if self.file_name and self.file_name.endswith('.gvar'):
      gvar = os.path.basename(self.file_name)
      if gvar and gvar.endswith('.gvar'):
        gvar = gvar[:-5]
        self.on_done(gvar)
    elif name and name.endswith('.gvar'):
      if name.endswith('.gvar'):
        gvar = name[:-5]
        self.on_done(gvar)
    else:
      self.window.show_input_panel("Gvar ID:", "", self.on_done, None, None)

  def on_done(self, text):
    if text:
        gvar = text.replace('\n','').strip()[:36]
        name = text[36:].replace('.gvar','').replace('\n','')
        view = self.window.active_view()
        getStatus = 0
        if gvar:
            if len(gvar)==36:
              get, getStatus = avraeREST("GET", "customizations/gvars/" + gvar, ttl_hash=get_ttl_hash(5))
              if view.file_name() and gvar in view.file_name():
                view.run_command('select_all')
                view.run_command('right_delete')
              else:
                view = self.window.new_file()
                view.set_name(gvar + name + '.gvar')
                view.set_syntax_file("Packages/Avrae Utilities/Draconic.sublime-syntax")
              view.run_command('append', {'characters' : get.json().get('value')})
            else:
              self.view.show_popup("<b>Something went wrong</b><br>Invalid Gvar ID - " + gvar, max_width=500)

class collectionGet(sublime_plugin.WindowCommand):

  def run(self):
    self.file_name = self.window.active_view().file_name()
    if self.file_name and self.file_name.endswith('collection.id'):
      with open(self.file_name) as f:
        collection = json.load(f)
      return self.on_done(collection.get('collection'))
    self.window.show_input_panel("Collection ID:", "", self.on_done, None, None)

  def on_done(self, text):
    if text:
      view = self.window.active_view()
      get, getStatus = avraeREST("GET", "workshop/collection/" + text + '/full', ttl_hash=get_ttl_hash(5))
      view.set_syntax_file("Packages/Avrae Utilities/Draconic.sublime-syntax")
      data = get.json()['data']
      id_dict = {"name": data['name'], 
                 "collection": text, 
                 "aliases": {},
                 "snippets": {}}
      for alias in data.get('aliases', {}):
        id_dict['aliases'][alias.get('name')] = alias.get('_id')
        for subalias in alias.get('subcommands'):
          id_dict['aliases'][alias.get('name') + ' ' + subalias.get('name')] = subalias.get('_id')
      for alias in data.get('snippets', {}):
        id_dict['snippets'][alias.get('name')] = alias.get('_id')
      if view.file_name() and 'collection.id' in view.file_name():
        view.run_command('select_all')
        view.run_command('right_delete')
      else:
        view = self.window.new_file()
        view.set_name('collection.id')
      view.run_command('append', {'characters' : json.dumps(id_dict, indent=2)})

class workshopContentGet(sublime_plugin.WindowCommand):

  def run(self, contentType):
    self.id = None
    self.contentType = contentType
    self.contentPlural = 'aliases' if self.contentType == 'alias' else 'snippets'
    self.file_name = self.window.active_view().file_name() or ""
    collection_file = os.path.split(self.file_name)[0] + "\\collection.id"
    if self.file_name and os.path.exists(collection_file):
      with open(collection_file) as f:
        collection = json.load(f)
        if os.path.splitext(os.path.split(self.file_name)[1])[0] in collection[self.contentPlural]:
          self.id = collection[self.contentPlural][os.path.splitext(os.path.split(self.file_name)[1])[0]]
          return self.on_done(self.id)
    self.window.show_input_panel("{} ID:".format(self.contentType.title()), "", self.on_done, None, None)

  def on_done(self, content_id):
    if content_id:
      view = self.window.active_view()
      get, getStatus = avraeREST("GET", "workshop/{}/".format(self.contentType) + content_id, ttl_hash=get_ttl_hash(5))
      view.set_syntax_file("Packages/Avrae Utilities/Draconic.sublime-syntax")
      data = get.json()['data']
      self.name = data['name']
      if self.id:
        view.run_command('select_all')
        view.run_command('right_delete')
        view.run_command('append', {'characters' : data['code'].replace('\r','')})
      else:
        view = self.window.new_file()
        subalias = False
        if data.get('parent_id'): # is it a subalias? if so, collect the names of the parent alias and prepend to file name
          subalias = True
          parent_id = data['parent_id']
          while subalias:
            get, getStatus = avraeREST("GET", "workshop/{}/".format(self.contentType) + parent_id, ttl_hash=get_ttl_hash(5))
            parentData = get.json()['data']
            self.name = parentData['name'] + ' ' + self.name
            subalias = bool(parentData['parent_id'])
        view.set_name(self.name + '.{}'.format(self.contentType))
        view.set_syntax_file("Packages/Avrae Utilities/Draconic.sublime-syntax")
        view.run_command('append', {'characters' : data['code'].replace('\r','')})


class workshopContentUpdate(sublime_plugin.WindowCommand):

  def run(self, contentType):
    self.contentType = contentType
    self.contentPlural = 'aliases' if self.contentType == 'alias' else 'snippets'
    self.view = self.window.active_view()
    self.payload = self.view.substr(sublime.Region(0, self.view.size()))
    self.id = None
    self.name = None
    self.collection_name = None
    self.file_name = self.window.active_view().file_name()
    if self.file_name and os.path.exists(os.path.split(self.file_name)[0] + "\\collection.id"):
      with open(os.path.split(self.file_name)[0] + "\\collection.id") as f:
        collection = json.load(f)
        if os.path.splitext(os.path.split(self.file_name)[1])[0] in collection[self.contentPlural]:
          self.name = os.path.splitext(os.path.split(self.file_name)[1])[0]
          self.id = collection[self.contentPlural][self.name]
          self.collection_name = collection['name']
          return self.on_done(self.id)

  def on_done(self, content_id):
    if content_id:
      view = self.window.active_view()
      get, getStatus = avraeREST("post", endpoint = "workshop/{}/".format(self.contentType) + content_id + '/code', payload = json.dumps({"content": self.payload}), ttl_hash=get_ttl_hash(5))
      self.version = get.json()['data']['version']
      get, getStatus = avraeREST("put", endpoint = "workshop/{}/".format(self.contentType) + content_id + '/active-code', payload = json.dumps({"version": self.version}), ttl_hash=get_ttl_hash(5)) 
      if getStatus in (200, 201):
        self.window.active_view().show_popup(
          '''<b>Successfully Updated Workshop Content:</b>
          <ul>
            <li>
              <b>Collection:</b> {}
            </li>
            <li>
              <b>Type:</b> {}
            </li>
            <li>
              <b>Name:</b> {}
            </li>
            <li>
              <b>ID:</b> {}
            </li>
          </ul>'''.format(self.collection_name, self.contentType.title(), self.name, self.id), max_width=400)      


@lru_cache()
def avraeREST(type: str, endpoint: str, payload: str = None, ttl_hash = None):
  del ttl_hash
  if payload is None:
    payload = ""
  token = sublime.load_settings('Avrae.sublime-settings').get('token')
  headers['Authorization'] = token
  url = '/'.join(["https://api.avrae.io", endpoint]).strip('/')

  try:
    request = requests.request(type.upper(), url , headers=headers, data = payload)
    requestStatus = request.status_code
  except:
    if requestStatus==403:
      print("Unsuccessfully {}: {} - Double check your token".format(type.upper(), endpoint), requestStatus)
      view.show_popup("<b>Something went wrong - Status Code 403</b><br>Double check your token.", max_width=500)
    if requestStatus==404:
      print("Unsuccessfully {}: {} - Invalid endpoint".format(type.upper(), endpoint), requestStatus)
      view.show_popup("<b>Something went wrong - Status Code 404</b><br>Invalid ID", max_width=500)

  if requestStatus in (200, 201):
    print("Successfully {}: {}".format(type.upper(), endpoint), requestStatus)
    sublime.status_message("Successfully {}: {}".format(type.upper(), endpoint))

  return request, requestStatus

def get_ttl_hash(seconds=900):
    """Return the same value within `seconds` time period"""
    return round(time.time() / seconds)


class makeAttack(sublime_plugin.WindowCommand):

  def run(self):
    sel = self.window.active_view().substr(self.window.active_view().sel()[0])
    sel = json.loads(sel)
    # If we just have the automation portion selected, name it test
    if isinstance(sel, list):
      sublime.set_clipboard('!a import {"name": "Test", "automation":' + json.dumps(sel) + ',"_v": 2}')
    # Otherwise try to grab the name of the actual attack/action
    elif isinstance(sel, dict):
      sel = {"name": sel.get('name'), "automation": sel.get('automation'), "_v": 2}
      sublime.set_clipboard('!a import ' + json.dumps(sel))


