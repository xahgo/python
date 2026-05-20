import sys
import os
from pdfminer_custom.high_level import extract_font
from xfile import XFile
from xjson import XJson

# print("PYTHON EXE =", sys.executable)
# print("sys.path =", sys.path)

# high_level.py가 있는 폴더 추가
# sys.path.append(os.path.join(os.path.dirname(__file__), "..\\pdfminer_custom\\src\\pdfminer_custom"))

# dic_test: dict[int, dict] = {}
# for i in range(1, 11):
#   dic: dict[int, str] = {}
#   for k, c in enumerate(range(ord('a'), ord('z') + 1)):
#     dic[k] = chr(c)
#   dic_test[i] = dic
#
# fullpath = f"{XFile.getcwd()}\\dic_test.json"
# XJson.save_json_file(dic_test, fullpath)
# print(f"saved json: path={fullpath}")


# text = extract_text(pdf_path)
# print(text)

def extract_cid2unicode() -> None:
  # use: xxx.py "c:\\src\\xxx.pdf c:\\dst//xxx.json(생략시 pdf와 동일위치)"
  print(f'__name__={__name__}')
  print(f'argv.len={len(sys.argv)}')
  if __name__ == "__main__" and len(sys.argv) == 1:
    # 파이참에서 직접 실행(테스트용)
    print("\n");
    path_src = XFile.getcwd()
    fullpath_pdf = f"{path_src}/_jjan_20.pdf"
    # fullpath_pdf = f"{path_src}/Sch_Das.pdf"
    pdf_filename = XFile.get_filename(fullpath_pdf)
    path_output = f"{path_src}\\{XFile.get_file_title(pdf_filename)}.json"
    print(f"pdf path={fullpath_pdf}")
  else:
    # 외부모듈에서 호출
    if len(sys.argv) >= 2:
      # pdf(src)의 풀패스를 받음.
      fullpath_pdf = sys.argv[1]
      path_src = XFile.get_path(fullpath_pdf)
      print(f"pdf path={fullpath_pdf}")
      # json(dst)의 패스
      if len(sys.argv) == 2:
        # 출력json이름을 생략하면 pdf이름.json으로 자동생성된다.
        pdf_filename = XFile.get_filename(fullpath_pdf)
        path_output = f"{path_src}\\{XFile.get_file_title(pdf_filename)}.json"
      elif len(sys.argv) == 3 and sys.argv[2] != 'json_test':
        # 출력 json이름을 지정했으면 그 이름으로 출력
        path_output = sys.argv[2]
      else:
        # 수동 파일명 지정 테스트 모듈
        path = XFile.get_path(fullpath_pdf)
        file_title = XFile.get_file_title(fullpath_pdf)
        path_output = f"{path}/cid_{file_title}.json"
    else:
      print('usage: extract_cid2unicode.py "c:\\target\\xxx.pdf" "c:\\target\\cid_xxx.json"')
      return
  # cidunicode 추출
  my_pdf_font = extract_font(fullpath_pdf)
  # save json
  print(f"try json save. path={path_output}")
  XJson.save_json_file(my_pdf_font.to_dict(), path_output)
  # c#측에서 path_output으로 성공여부 가리고 '='로 split해서 씀.
  print(f"path_output={path_output}")


extract_cid2unicode()
sys.stdout.flush()
exit(0)