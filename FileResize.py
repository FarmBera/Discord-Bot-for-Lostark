# import sys
# import os
from PIL import Image
# from MainList import pict_dir
from MainList import new_pict_dir as pict_dir

# # Get the parent directory
# parent_dir = os.path.dirname(os.path.realpath(__file__))

# # Add the parent directory to sys.path
# sys.path.append(parent_dir)


saveFPath = 'image_real/image_se/'

# Picture Directory
def Resize():
    # trim_text = None
    for trim_text in pict_dir.keys():
        try: 
            # trim_text = "[놀자에요"
            bef_image = Image.open(pict_dir[trim_text])
            image = bef_image.resize((150, 150))
            # image.save(f"{pict_dir[trim_text]}")
            image.save(f"{saveFPath}{trim_text}")
            print(bef_image)
        except Exception as e:
            print(trim_text)
            print(e)

def CheckDuplicate(): 
    NEW_PICT = []
    for i in pict_dir:
        NEW_PICT.append(i)
    print(NEW_PICT)
    # NEW_PICT = [1, 1, 2, 5, 6, 3, 7, 78, 5, 76, 4,3, 4, 34 ]
    
    # Solution 1
    # temp = [] # 처음 등장한 값인지 판별하는 리스트
    duplicated = [] # 중복된 원소만 넣는 리스트
    # for i in NEW_PICT:
    #     if i not in temp: # 처음 등장한 원소
    #         temp.append(i)
    #     else:
    #         if i not in duplicated: # 이미 중복 원소로 판정된 경우는 제외
    #             duplicated.append(i)
    # print(duplicated) # [1, 2] # 2회 이상 등장한 값들만 담긴 리스트
    
    # Solution 2
    duplicated_count = {} # 각 원소의 등장 횟수를 카운팅할 딕셔너리
    for i in NEW_PICT:
        try: # 이미 등장한 값의 경우
            duplicated_count[i] += 1
        except: # 처음 등장한 값의 경우
            duplicated_count[i] = 1
    print(duplicated_count) # {'a': 2, 'b': 2, 'c': 1, 'd': 1}
    for k, v in duplicated_count.items():
        if v >= 2: # n회 이상 등장한 원소로도 변경 가능
            duplicated.append(k)
    print(duplicated) # ['a', 'b']


def Length(): 
    print(f"length >> {len(pict_dir)}")

#################
# CheckDuplicate()
Resize()
print(len(pict_dir))
Length()
