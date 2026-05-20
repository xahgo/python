import json as Json
from xfile import XFile


class XJson:
  # json타입의 dictionary를 파일로 쓴다
  @staticmethod
  def save_json_file(dic_json, fullpath, encoding="utf-8", default=None):
    # 폴더가 없다면 만든다. 이미 폴더가 있어도 에러가 나지 않는다.
    path = XFile.get_path(fullpath)
    XFile.make_dir(path)
    with open(fullpath, "w", encoding=encoding) as json_file:
      Json.dump(dic_json, json_file, indent=2, ensure_ascii=False, default=default)

  # json파일을 읽어 json타입 dictonary로 리턴한다.
  @staticmethod
  def load_json_file(fullpath, encoding=None):
    with open(fullpath, "r", encoding=encoding) as json_file:
      dic_json = Json.load(json_file)
    return dic_json
