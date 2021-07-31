import json

class Parser(object):
  def __init__(self,obj):
    self.__dict__ = json.loads(obj)