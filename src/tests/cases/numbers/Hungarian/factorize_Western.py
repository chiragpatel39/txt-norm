# Factorizer for Western numbers. 
# One '0' preserved only if there are no non-zero digits.
#
# It should let any text through, but only factorize numbers that appear as a part of separate tokens, 
# right after a whitespace character (space, tab, or new line);
# suffixes are left unchanged.
# 
# E.g. "The 12th" becomes "The 1<E1>2th".
# But "A12" and "[12]" will remain unchanged.
#
# Usage: factorize_Western.py input.txt factorized_output.txt
#
# Author: geza.kiss@cslu.ogi.edu (Geza Kiss)

import sys,re 

# create factorization symbol
def getFactor(iFactor):
  return '<E' + str(iFactor) + '>'

# factorize number
def factorize(sNumber):
  sFactorizedNumber = ''
  nLen = len(sNumber)
  bNonZeroEncountered = False
  for iPos in range(nLen):
    iFactor = nLen - iPos - 1
    cDigit = sNumber[iPos]
    if 0 != int(cDigit) or (not bNonZeroEncountered and iPos == nLen - 1):
      sFactorizedNumber += cDigit
      bValueInGroup = True
      bNonZeroEncountered = True
    if 0 < iFactor:
      iFactorInGroup = iFactor % 3
      if 0 != iFactorInGroup:
        iFactor = iFactorInGroup
      if 0 != int(cDigit) or (0 == iFactorInGroup and bValueInGroup):
        sFactorizedNumber += getFactor(iFactor) 
        if 0 == iFactorInGroup:
          bValueInGroup = False
  return sFactorizedNumber

# create factorized denominator
def getDenominator(iFactor):
  return '<denominator>' + factorize(str(pow(10, iFactor)))

if '__main__'==__name__:
  lsArgv=sys.argv[1:]
  iArgc=len(lsArgv)
  
  if 2 != iArgc:
    raise ValueError("Usage: factorize.py <in: numbers text file> <out: factorize text file>")
  sNumberFilename = lsArgv[0]
  sFactoredFilename = lsArgv[1]

  fIn = open(sNumberFilename, 'rt')
  fOut = open(sFactoredFilename, 'wb')
  reNumber = re.compile('[0-9]+')
  bValueInGroup = False
  for sLine in fIn: # process lines of file
    sFactorizedLine = ''
    lsExpr = sLine.split()
    for sExpr in lsExpr: # process tokens
      if sFactorizedLine:
        sFactorizedLine += ' '
      oMatchNumber = reNumber.match(sExpr)
      if not oMatchNumber:
        sFactorizedLine += sExpr # if it doesn't start with digits
        continue
      sNumber = oMatchNumber.group()    # the number
      sRemainder = sExpr[len(sNumber):] # suffix, etc.
      
      # create output
      sFactorizedLine += factorize(sNumber)
      if sRemainder and ',' == sRemainder[0]: # it may be a decimal fraction
        oMatchNumber = reNumber.match(sRemainder[1:])
        if oMatchNumber: # it is a decimal fraction
          sNumber = oMatchNumber.group() # part after the decimal separator
          sRemainder = sRemainder[1+len(sNumber):] # suffix, etc.
          sFactorizedLine += ',' 
          sFactorizedLine += factorize(sNumber)
          # out of ...; append after special symbol 
          sFactorizedLine += getDenominator(len(sNumber))
      sFactorizedLine += sRemainder
    fOut.write(sFactorizedLine + '\n')
  fOut.close()
  fIn.close()
