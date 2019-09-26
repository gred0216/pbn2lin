import os
import glob
import re
import time


def main():
    # Edit .pbn
    # Find all .pbn files
    pbns = glob.glob('*.pbn')
    for pbn in pbns:
        with open(pbn, 'r+') as pbn_original:
            original = pbn_original.read()
            # Only four kinds of information are needed
            # Find the information of each board
            # Board number
            board = '\[Board \"\d{1,}\"\]'
            mat_board = re.findall(board, original, re.DOTALL)
            # Dealer: N/S/E/W
            dealer = '\[Dealer \"[NSEW]\"\]'
            mat_dealer = re.findall(dealer, original, re.DOTALL)
            # Vulnerable: None/NS/EW/All
            vulnerable = '(\[Vulnerable \"(None|NS|EW|All)\"\])'
            mat_vulnerable = re.findall(vulnerable, original, re.DOTALL)
            # Deal: hands of four players
            deal = '\[Deal \"[NSEW]:.{67}\"\]'
            mat_deal = re.findall(deal, original, re.DOTALL)
            # Add this line at the beginning of the file
            outtxt = ['% Dealer4 ver 4.42']
            # Add these three lines before each board
            addtxt = ['\n[Event ""] \n', '[Site ""] \n', '[Date ""] \n']
            for i in range(len(mat_board)):
                # Add the boards into the list
                outtxt += addtxt
                outtxt.append(mat_board[i] + '\n')
                outtxt.append(mat_dealer[i] + '\n')
                outtxt.append(mat_vulnerable[i][0] + '\n')
                outtxt.append(mat_deal[i] + '\n')
            # Clear the file and write in the list
            pbn_original.seek(0)
            pbn_original.truncate()
            pbn_original.writelines(outtxt)
        # Execute .pbn file to generate .lin file
        os.startfile(pbn)
        time.sleep(2)
        os.system('TASKKILL /IM NetBridgeVu.exe')

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
