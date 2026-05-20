import datetime

class XUtil:
  @staticmethod
  def generate_string_datetime():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

  @classmethod
  def find(cls, ary=None, val=None, filter=None):
    # return next(filter(lambda e: e['item'] == 'hello', my_list), None)
    if filter is None:
      # 리스트 컴프리헨션을 사용한 방법
      return next((e for e in ary if e == val), None)
    # filter() 함수를 사용한 방법
    return next(filter, None)

  @classmethod
  def find2(cls, ary=None, val=None, filter=None):
    # return next(filter(lambda e: e['item'] == 'hello', my_list), None)
    if filter is None:
      # 리스트 컴프리헨션을 사용한 방법
      return next(((i, e) for i, e in enumerate(ary) if e == val), None)
    # filter() 함수를 사용한 방법
    return next(filter, None)

  @classmethod
  def find_idx(cls, ary=None, val=None, compare=None):
    if compare is None:
      return next((i for i, e in enumerate(ary) if e == val), -1)
    return next((i for i, e in enumerate(ary) if compare(e, val)), -1)
    # return next(filter, -1)

  @classmethod
  def slice_dic(cls, dic, idxS, size):
    """
    dictionary를 부분만 취해서 slice한다.
    :param dic: 대상 사전
    :param idxS: dic의 slice 시작 인덱스
    :param size: dic의 idxS로부터 크기
    :return: {key: value}의 사전
    """
    return {key: value for i, (key, value) in enumerate(dic.items())
            if idxS <= i < idxS + size}

  @classmethod
  def has_ary(cls, ary, val):
    """
    ary에 val값을 가진 요소가 있는지 검사한다.
    :param ary: 대상이 될 리스트 혹은 배열
    :param val: 찾을 값
    :return: 있으면 True, 없으면 False
    """
    for e in ary:
      if e == val:
        return True
    return False

  @classmethod
  def has_dic(cls, dic, key):
    """
    dic안에 key가 있는지
    :param dic: 대상 사전
    :param key: 검색 키
    :return: True/False
    """
    if key in dic:
      return True
    return False

