
def index_fnz_lnz(df):
    '''fuction that returns first non zero and last non zero for each AR
    input df: must be formatted '''
    index_fnz_lnz = []
    for col in df.columns:
        fnz=0
        i=0
        while df[col][i] == 0:
            i += 1
            fnz = i
        lnz=4018
        j=4018
        while df[col][j] == 0:
            j -= 1
            lnz = j
        #print(col, fnz, lnz)
        index_fnz_lnz.append((fnz,lnz))
    return index_fnz_lnz
