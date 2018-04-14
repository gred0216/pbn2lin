import os
import glob
import re
import time


def main():
    # Edit .pbn
    pbns = glob.glob("*.pbn")
    for pbn in pbns:
        with open(pbn, 'r+') as pbn_original:
            original = pbn_original.read()
            pat = '\[Board.*?\[Deal\ .*?"\]'
            mat = re.findall(pat, original, re.DOTALL)
            outtxt = ['% Dealer4 ver 4.42']
            addtxt = ['\n[Event ""] \n', '[Site ""] \n', '[Date ""] \n']
            for i in range(len(mat)):
                outtxt += addtxt
                outtxt.append(mat[i])
            pbn_original.seek(0)
            pbn_original.writelines(outtxt)
        # Execute .pbn file to generate .lin file
        os.startfile(pbn)
        time.sleep(1)
        os.system("TASKKILL /IM NetBridgeVu.exe")

    # Edit .lin
    lins = glob.glob('*.lin')
    for lin in lins:
        with open(lin, 'r+') as lin_original:
            lintxt = lin_original.readlines()
            # Make "mn||" to a newline in line 7
            lintxt[6:6] = ["mn||\n"]
            lintxt[7] = lintxt[7].replace("mn||", "")
            # Copy open room boards to close room
            bd_open = lintxt[7:]
            bd_close = [i.replace("|o", "|c")
                        if "|o" in i else i for i in bd_open]
            lintxt += bd_close
            lin_original.seek(0)
            lin_original.writelines(lintxt)


if __name__ == '__main__':
    main()
