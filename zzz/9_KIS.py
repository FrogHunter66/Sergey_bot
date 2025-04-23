def finder_int(lst: list):
    for s in lst:
        try:
            c = int(s)
            return c
        except ValueError:
            pass
    for s in lst:
        for c in s.split('\n'):
            try:
                n = int(c)
                return n
            except ValueError:
                pass
    return None


def finder_word(s: str):
    s_new = s.replace(" ", "").replace("]", "")\
        .replace(".", "").replace("}", "").replace("\n", "")
    return s_new


def main(s: str):
    lst_main = list(map(str, s.split("]]")))
    lst_main.pop(-1)
    d = dict()
    for ptr in lst_main:
        lst_new = list(map(str, ptr.split("=:")))
        lst_new.pop(-1)
        lst_new = ''.join(lst_new)
        lst_new = list(map(str, lst_new.split(" ")))
        num = finder_int(lst_new)
        right = list(map(str, ptr.split("=:")))
        right.pop(0)
        right = ''.join(right)
        word = finder_word(right)
        d[word] = num
    return d

print("\n\n-----ANSWER-----")
print(main("{{[[ variable -9128 =:zaama_898 ]]. [[ variable 8602 =:\natusza_118]].}}"))
print("----------------------------------")
print(main("{{ [[ variable -5013 =: cear ]]. [[variable -6416 =: lelele_153 ]]. }}"))
print("----------------------------------")
print(main("{{[[variable 5911 =: soce_193 ]].[[ variable 3968 =:isinat_718 ]]. [[\nvariable 3481 =:ustiti_211 ]]. [[ variable 2390 =:tira]].}}"))
print("----------------------------------")
print(main("{{ [[ variable 3169 =: dimaen]].[[ variable 6381=:orbive_782 ]].}}"))
print("----------------------------------")
print(main("{{ [[variable -5228 =:ange]]. [[ variable 3188=: ralaus]].[[variable\n-9284=:beed_27]].}}"))
print("----------------------------------")
print(main("{{ [[variable -5228 =:ange]]. [[ variable 3188=: ralaus]].[[variable\n-9284=:beed_27]].}}"))
