import inspect
import os
import objgraph

# Нужно установить Graphviz и objgraph,
# Graphviz установил с сайта, с pip он почему то не заработал

FILENAME = "ProjectIntrospectionGraph"  # Без расширения


F = set()
C = set()
M = set()

L = [len(F), len(C), len(M)]


def relen():
    L[0] = len(F)
    L[1] = len(C)
    L[2] = len(M)


def get_s2(obj):
    for attr in dir(obj):
        if '__' not in attr:
            # эх било би время на оптимизацию этого говна...
            # блять тут можно было inspect.getmembers(obj, inspect.isSOMETHING)
            if inspect.isfunction(getattr(obj, attr)):
                F.add(getattr(obj, attr))
            if inspect.isclass(getattr(obj, attr)):
                C.add(getattr(obj, attr))
            if inspect.ismodule(getattr(obj, attr)):
                M.add(getattr(obj, attr))

    if len(F) != L[0]:
        L[0] = len(F)
        for f in F.copy():
            get_s2(f)
    if len(C) != L[1]:
        L[1] = len(C)
        for c in C.copy():
            get_s2(c)
    if len(M) != L[2]:
        L[2] = len(M)
        for m in M.copy():
            get_s2(m)


def generate_graph(filename=FILENAME):
    # Generates project graph into file
    for k, v in globals().copy().items():
        get_s2(v)

    # print("Total: {} objects".format(sum(L)))

    summary = set()

    # patter = re.compile(r'(.*Python\d{0,5}\\Lib\\.*)|(<.*)')

    def is_standard(o):
        try:
            s = inspect.getsourcefile(o)
            if "\Python\\" in s and "\Lib\\" in s or "<" in s:
                return True
            return False
        except:
            return False

    for d in [F, C, M]:
        for e in d:
            if not is_standard(e):
                summary.add(e)
    # summary.update(F)
    # summary.update(C)
    # summary.update(M)
    print("Total: {} objects".format(len(summary)))


    for o in summary:
        if not is_standard(o):
            try:
                print(is_standard(o), inspect.getsourcefile(o))
            except:
                pass


    objgraph.show_backrefs(list(summary),
                           filter=lambda x: inspect.isclass(x) or inspect.isfunction(x) or inspect.ismodule(x) and not is_standard(x),
                           refcounts=True,
                           filename=filename + ".dot",
                           max_depth=35,
                           too_many=3)

    cmd = "dot -Tsvg -Kcirco .\{}.dot -o {}.svg".format(filename, filename)

    os.system(cmd)
    os.remove(".\{}.dot".format(filename))


if __name__ == '__main__':
    """Создает граф с именем FILENAME.svg в рабочей папке"""
    generate_graph()