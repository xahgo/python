from typing import Optional, ClassVar
from dataclasses import dataclass, asdict


@dataclass
class MyPDFFontData:
  data_id_global: ClassVar[int] = 0
  # fontdata cache. key: fontdata_id, val: MyPDFFontData
  dic_fontdata: ClassVar[dict[int, "MyPDFFontData"]] = {}
  data_id: int
  font_type: str  # ex: 'Type1'
  font_id: str  # ex: 'F1'
  basefont: str
  fontname: str

  def __init__(self, type, font_id, basefont, fontname):
    MyPDFFontData.data_id_global += 1
    self.data_id: int = MyPDFFontData.data_id_global
    self.font_type: str = type  # ex: 'Type1'
    self.font_id: str = font_id  # ex: 'F1'
    self.basefont: str = basefont
    self.fontname: str = fontname

  @classmethod
  def to_dict(cls) -> dict[int, dict]:
    dic_json = {}
    for data_id, fontdata in cls.dic_fontdata.items():
      dic_json[data_id] = asdict(fontdata)
    return dic_json

  # DebuggerDisplay
  def __repr__(self):
    return f"id:{self.data_id} {self.font_type} fid={self.font_id} name={self.fontname}"

  def __eq__(self, other):
      if isinstance(other, MyPDFFontData):
        return self.EqualData(other.font_type, other.font_id, other.basefont, other.fontname)
      else:
        return False

  # data가 일치하는지 검사
  def EqualData(self, type, font_id, basefont, fontname) -> bool:
    if self.font_type != type:
      return False
    if self.font_id != font_id:
      return False
    if self.basefont != basefont:
      return False
    if self.fontname != fontname:
      return False
    return True

  @classmethod
  def add(cls, font_type: str, font_id: str, basefont: str, fontname: str) -> Optional["MyPDFFontData"]:
    """
    캐시에 추가하기
    :param font_type: ex: 'Type1'
    :param font_id:   ex: 'F1'
    :param basefont: str
    :param fontname: str
    :return: MyPDFFontData 객체
    """
    # 이미 있으면 그걸 리턴
    for fontdata in cls.dic_fontdata.values():
      if fontdata.font_type == font_type and fontdata.font_id == font_id and \
            fontdata.basefont == basefont and fontdata.fontname == fontname:
        return fontdata

    # 새로 생성
    fontdata = MyPDFFontData(font_type, font_id, basefont, fontname)
    cls.dic_fontdata[fontdata.data_id] = fontdata
    return fontdata

  @classmethod
  def get(cls, fontdata_id) -> Optional["MyPDFFontData"]:
    """
    캐시에서 가져오기
    :param fontdata_id:
    :return: MyPDFFontData객체
    """
    return cls.dic_fontdata[fontdata_id]
    # return next((fontdata for fontdata in cls.dic_fontdata.values() if fontdata.data_id == fontdata_id), None)


class MyPDFFontObj:
  # ci2unicode만 id로 넘긴것은 dict
  def __init__(self, objid: int, fontdata: MyPDFFontData, cid2unicode_id: int, my_pdf_font):
    self.objid: int = objid
    # ref로 보관
    self.fontdata: MyPDFFontData = fontdata
    self.cid2unicode_id: int = cid2unicode_id
    self.cid2unicode = my_pdf_font.get(cid2unicode_id) # 디버깅 편의상 ref로 받아둠.

  # DebuggerDisplay
  def __repr__(self):
    return f"id:{self.objid} {self.fontdata} cid2unicode({self.cid2unicode_id})={self.cid2unicode}"

  def to_dict(self) -> dict[str, int]:
      return {"fontdata_id": self.fontdata.data_id,
              "cid_id": self.cid2unicode_id,
             }


class MyPDFFont:
  cid_id_global: ClassVar[int] = 0

  def __init__(self):
    # cidary cache. key: cid_idx, val: dict_cid2unicode
    self.dic_cidary: dict[int, dict[int, str]] = {}
    # objid: fontobj
    self.dic_font_obj: dict[int, MyPDFFontObj] = {}
    # dic_used_font: ClassVar[dict[int, MyPDFFontObj]] = {}
    self.dic_pageno_fontobjs_in_page: dict[int, dict[int, MyPDFFontObj]] = {}
    # make total dict
    self.dic_total: dict[str, dict] = {"fontdatas": MyPDFFontData.dic_fontdata,
                                       "cids": self.dic_cidary,   # dict[int, dict[int, str]]
                                       "pages": self.dic_pageno_fontobjs_in_page}  # dict[int pageno, dict[int objid, MyPDFFontObj]]

  def to_dict(self) -> dict[str, dict]:
    dic_json: dict[str, dict] = {}
    for key, dic in self.dic_total.items():
      dic_json[key] = {}

    dic_json["fontdatas"] = MyPDFFontData.to_dict()
    _dic_cidary: dict[int, dict[int, str]] = {}
    for key, dic in self.dic_cidary.items():
      _dic_cidary[key] = dict(sorted(dic.items()))
    dic_json["cids"] = _dic_cidary
    # dic_json["cids"] = self.dic_cidary
    dic_json["pages"] = self.to_dict_pages()
    return dic_json

  def to_dict_pages(self):
    dic_json: dict[int, dict] = {}
    for pageno, dic_fontobj in self.dic_pageno_fontobjs_in_page.items():
      dic_fonts: dict[int, dict] = {}
      for objid, fontobj in dic_fontobj.items():
        dic_fonts[objid] = fontobj.to_dict()
      dic_json[pageno] = dic_fonts
    return dic_json

  def add_dic_fontdata(self, dic_fontdata: dict[int, MyPDFFontData]):
    self.dic_total["fontdatas"] = dic_fontdata

  def add_cidary(self, cid2unicode: dict[int, str]) -> int:
    # 같은 값을 가진 dict가 있는지 검사해서 있으면 그것의 cid_idx를 리턴하고, 없으면 중복되지 않게 딕셔너리에 쌓는다.
    key_val = next(((cid_id, cid_dict) for cid_id, cid_dict in self.dic_cidary.items() if cid_dict == cid2unicode), None)
    if key_val:
      return key_val[0] # cid_id

    MyPDFFont.cid_id_global += 1
    self.dic_cidary[MyPDFFont.cid_id_global] = cid2unicode.copy()  # dict의 복사본을 넣는다.
    return MyPDFFont.cid_id_global

  def get(self, cid2unicode_id) -> Optional[dict[int, str]]:
    """
    캐시에서 가져오기
    :param cid2unicode_id:
    :return: dict cid2unicode
    """
    return self.dic_cidary[cid2unicode_id]

  def add_used_font(self, pageno, objid, fontdata, cid_id):
    font_obj = MyPDFFontObj(objid, fontdata, cid_id, self)
    self.dic_font_obj[objid] = font_obj
    # cls.dic_used_font[objid] = font_obj
    # 같은 아이디의 다른데이터가 들어오는지 확인필요
    self.dic_pageno_fontobjs_in_page[pageno] = self.dic_font_obj;




