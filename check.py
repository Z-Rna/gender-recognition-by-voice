from inf141276_inf141304 import *

def check():
    good = 0
    path = sys.argv[1]
    for r, d, f in os.walk(path):
        for file in f:
            len_f = len(f)
            if '.wav' in file:
                i = os.path.join(r, file)
                w, signal = read_signal(i)
                freq = hps(signal, w)
                if(recognize_gender(freq) == i[-5:-4]):
                    good += 1
    print(f"effectiveness: {round(good * 100 / len_f, 2)}%")

if __name__ == '__main__':
    check()