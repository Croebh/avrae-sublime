
import json
import sublime, sublime_plugin, os, webbrowser
import requests
from functools import lru_cache
import time
import sys, traceback



headers = {
            'Authorization': "",
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'Content-Type': 'application/json',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty'
          }


url = "https://api.avrae.io/customizations/gvars/"


class gvarUpdateCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    file_name  = self.view.file_name()
    name       = self.view.name()
    getStatus  = 0
    postStatus = 0
    gvar       = None
    payload    = self.view.substr(sublime.Region(0, self.view.size()))

    if name and name.endswith('.gvar'):
      if name.endswith('.gvar'):
        gvar = name[:36]
    elif file_name:
        gvar = os.path.basename(file_name)
        if gvar and gvar.endswith('.gvar'):
            gvar = gvar[:36]

    if gvar and len(gvar)==36:
      try:
        get        = avraeREST("GET", "gvars", gvar, ttl_hash=get_ttl_hash(5))
        getStatus  = get.status_code
        newPayload = get.json()
        newPayload.update({"value":payload})

        post       = avraeREST("POST", "gvars", gvar, json.dumps(newPayload), ttl_hash=get_ttl_hash(5))
        postStatus = post.status_code

        if getStatus == 200 and postStatus == 200:
          sublime.status_message("Successfully updated Gvar: {}".format(gvar))
          self.view.show_popup("<b>Successfully updated Gvar:</b> {}".format(gvar), max_width=500)
        elif getStatus == 200 and postStatus == 403:
          self.view.show_popup("<b>Something went wrong - Status Code 403</b><br>Double check that you have edit permissions.", max_width=500)
      except:
        traceback.print_exc(file=sys.stdout)
        if getStatus == 403:
          self.view.show_popup("<b>Something went wrong - Status Code 403</b><br>Double check your token, and that you have edit permissions.", max_width=500)
        if getStatus == 404:
          self.view.show_popup("<b>Something went wrong - Status Code 404</b><br>Invalid Gvar ID + gvar", max_width=500)
    else:
      self.view.show_popup("<b>Something went wrong</b><br>Invalid Gvar ID - " + str(gvar), max_width=500)


class gvarGetCommand(sublime_plugin.WindowCommand):

  def run(self):
    file_name = self.window.active_view().file_name()
    name = self.window.active_view().name()
    self.view = self.window.active_view()
    if file_name and file_name.endswith('.gvar'):
      gvar = os.path.basename(file_name)
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
              try:
                get = avraeREST("GET", "gvars", gvar, ttl_hash=get_ttl_hash(5))
                getStatus = get.status_code
              except:
                if getStatus==403:
                  view.show_popup("<b>Something went wrong - Status Code 403</b><br>Double check your token.", max_width=500)
                if getStatus==404:
                  view.show_popup("<b>Something went wrong - Status Code 404</b><br>Invalid Gvar ID + gvar", max_width=500)

              if getStatus == 200:
                print("Successfully grabbed Gvar: {}".format(gvar), getStatus)
                sublime.status_message("Successfully grabbed Gvar: {}".format(gvar))
                view = self.window.new_file()
                view.set_name(gvar + name + '.gvar')
                view.set_syntax_file("Packages/Avrae/Draconic.sublime-syntax")
                view.run_command('append', {'characters' : get.json().get('value')})
            else:
              self.view.show_popup("<b>Something went wrong</b><br>Invalid Gvar ID - " + gvar, max_width=500)


@lru_cache()
def avraeREST(type: str, customization: str, id, payload: str = None, ttl_hash = None):
  del ttl_hash
  if payload is None:
    payload = ""
  token = sublime.load_settings('Avrae.sublime-settings').get('token')
  headers['Authorization'] = token
  url = '/'.join(["https://api.avrae.io/customizations", customization, id]).strip('/')
  print(url)
  return requests.request(type.upper(), url , headers=headers, data = payload)


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


