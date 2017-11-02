from os import walk, system
from os.path import join

def main():
    f = []
    f_name = ""
    for (dirpath, _, filenames) in walk('./tests'):
        for e in filenames:
            if e.endswith('.py'):
                f.append(join(dirpath, e))
                f_name = f_name + " " + join(dirpath, e)
    print(f_name)
    system("pytest %s" %f_name)
    #for e in f:
    #    list_f = ""
    #    system("py.test-3 %s" %e)

main()

