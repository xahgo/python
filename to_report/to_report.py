import os
import csv
from pathlib import Path
from datetime import datetime
from xfile import XFile
from xutil import XUtil


def target_file_process_tr(folder_name, folder_path, prefix_str, str_ext, date_start, rows):
    """
    Target파일(TXT, JSON)을 열어서 관련작업을 한 후 csv row에 추가한다.
    :return:
    """
    target_filename = f"{prefix_str}{folder_name}.{str_ext}"
    target_file_path = os.path.join(folder_path, target_filename)
    # target 파일존재 확인
    # 원본_foldername_HHMMSS.txt형태면 파일명을 특정할수 없어서 파일 오픈이 힘들다.
    # done.txt 여부로 하려니 TR_ 검사와 일관성이 떨어진다.
    # 원본_xxxx_hhmmsss.txt파일만 모아서 소팅을 한다음 젤처음 파일을 여는 방식도 있다.
    if os.path.exists(target_file_path):
        with open(target_file_path, "r", encoding="utf-8") as f:
            created_timestamp = os.path.getctime(target_file_path)  # 생성시간 (초 단위). 수정날짜로 하려면 os.path.getmtime
            created_datetime = datetime.fromtimestamp(created_timestamp)
            # 시작날짜보다 이전날짜는 거른다.
            if date_start is not None and created_datetime < date_start:
                return
            # Target 파일명
            text = f.read()
            char_count = len(text)
            manuscript_pages = int(round(char_count / 200, 2))
            # target파일의 생성일자(수정일자에서 생성일자로 바꿈)
            str_date = created_datetime.strftime("%Y/%m/%d")
            XFile.copy_file(target_file_path, f"{dir_report}\\{target_filename}")
    else:
        # target 파일이 없으면 skip
        return
    # CSV 행 구성
    rows.append([folder_name, "", manuscript_pages, str_date, 100000])


def target_file_process_diff(folder_name, folder_path, prefix_str, str_ext, date_start, rows):
    """
    Target파일(TXT, JSON)을 열어서 관련작업을 한 후 csv row에 추가한다.
    :return:
    """
    # target 파일존재 확인
    # 원본_foldername_HHMMSS.txt형태면 파일명을 특정할수 없어서 파일 오픈이 힘들다.
    # done.txt 여부로 하려니 TR_ 검사와 일관성이 떨어진다.
    # 원본_xxxx_hhmmsss.txt파일만 모아서 소팅을 한다음 젤처음 파일을 여는 방식도 있다.
    folder = Path(folder_path)
    files = [
        f.name for f in folder.glob(f"{prefix_str}*")
        if f.is_file()
    ]
    if len(files) == 0:
        return

    target_filename = f"{folder_name}.{str_ext}"
    target_file_path = os.path.join(folder_path, target_filename)
    if os.path.exists(target_file_path):
        with open(target_file_path, "r", encoding="utf-8") as f:
            created_timestamp = os.path.getctime(target_file_path)  # 생성시간 (초 단위). 수정날짜로 하려면 os.path.getmtime
            created_datetime = datetime.fromtimestamp(created_timestamp)
            # 시작날짜보다 이전날짜는 거른다.
            if date_start is not None and created_datetime < date_start:
                return
            # Target 파일명
            text = f.read()
            char_count = len(text)
            manuscript_pages = int(round(char_count / 200, 2))
            # target파일의 생성일자(수정일자에서 생성일자로 바꿈)
            str_date = created_datetime.strftime("%Y/%m/%d")
            XFile.copy_file(target_file_path, f"{dir_report}\\{target_filename}")
    else:
        # target 파일이 없으면 skip
        return
    # CSV 행 구성
    rows.append([folder_name, "", manuscript_pages, str_date, 100000])


def save_row_to_csv(header, rows, output_csv):
    # # TR리스트 CSV로 저장
    # output_csv = f'report_tr_{XUtil.generate_string_datetime()}.csv'
    full_path = Path(output_csv)
    # 부모 폴더 생성
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{output_csv} 파일이 생성되었습니다.")

# CSV 헤더
header = ["원제목", "저자명", "원고지매수", "작업일", "비용"]

# 현재 py 파일이 있는 디렉토리 기준
# base_dir = os.path.dirname(os.path.abspath(__file__))
date_start = datetime(2026, 3, 23)
base_dir = "C:\\Users\\xuzhu\\OneDrive\\문서\\카카오톡 받은 파일"
# base_dir = "C:\\Users\\xuzhu\\Documents\\카카오톡 받은 파일"
num_dir = len(os.listdir(base_dir))
dir_report = f"{base_dir}\\__report"
output_dir = "output"
XFile.make_dir(dir_report)

# 결과 데이터
rows_tr = []
rows_diff = []
# 전체날짜를 하려면 nul
# date_start: Optional[datetime] = None


# 하위 폴더 순회
for idx, folder_name in enumerate(os.listdir(base_dir)):
    folder_path = os.path.join(base_dir, folder_name)
    # 폴더가 아니면 skip
    if not os.path.isdir(folder_path):
        continue
    # __report 폴더 제외
    if folder_name[:2] == "__":
        continue

    # TR파일 처리
    target_file_process_tr(folder_name, folder_path, "TR_", "txt", date_start, rows_tr)

for idx, folder_name in enumerate(os.listdir(base_dir)):
    folder_path = os.path.join(base_dir, folder_name)
    # 폴더가 아니면 skip
    if not os.path.isdir(folder_path):
        continue
    # __report 폴더 제외
    if folder_name[:2] == "__":
        continue

    # blk파일 처리
    target_file_process_diff(folder_name, folder_path, "원본_", "txt", date_start, rows_diff)

# report_tr_date.csv 저장
save_row_to_csv(header, rows_tr, f'{output_dir}\\report_tr_{XUtil.generate_string_datetime()}.csv')
# report_diff_date.csv 저장
save_row_to_csv(header, rows_diff, f'{output_dir}\\report_diff_{XUtil.generate_string_datetime()}.csv')

