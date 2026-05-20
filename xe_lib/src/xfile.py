import os
import shutil


class XFile:
  @staticmethod
  def has_file(fullpath):
    return os.path.exists(fullpath)

  @staticmethod
  def get_filename(fullpath):
    return os.path.basename(fullpath)

  @staticmethod
  def get_file_title(fullpath):
    # os.path 모듈의 splitext 함수를 사용하여 확장자 분리
    filename = os.path.basename(fullpath)
    file_title, file_extension = os.path.splitext(filename)
    return file_title

  @staticmethod
  def get_path(fullpath):
    return os.path.dirname(fullpath)

  @staticmethod
  def make_dir(fullpath):
    from pathlib import Path
    path_obj = Path(fullpath)
    path_obj.mkdir(parents=True, exist_ok=True)

  @staticmethod
  def copy_file(path_src, path_dst):
    shutil.copy(path_src, path_dst)

  @staticmethod
  def save_string(text, fullpath):
    # 폴더가 없다면 만든다. 이미 폴더가 있어도 에러가 나지 않는다.
    path = XFile.get_path(fullpath)
    XFile.make_dir(path)
    with open(fullpath, "w", encoding="utf-8") as file:
      file.write(text)

  # 파이썬 스크립트가 실행된 현재폴더를 얻는다.
  @staticmethod
  def getcwd():
    return os.getcwd()