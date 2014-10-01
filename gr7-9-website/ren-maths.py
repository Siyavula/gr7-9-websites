import os, sys

if __name__ == "__main__":
    args = sys.argv[1]

    args = int(args)

    files = [f for f in os.listdir(os.curdir)]
    files.sort()

    for f in files:
        try:
            if 'mathe' in f:
                grade, subject, N = f.split('-')
            else:
                grade, subject, N, afr = f.split('-')
        except:
            continue
        if N.startswith(str(args)):
            os.system("mv {} {}".format(f, f + '.backup'))
            args += 1

