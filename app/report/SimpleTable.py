###############################################################################
# Given an array of MemberStats objects, print various reports
###############################################################################

from prettytable import PrettyTable
from app.MemberStats import MemberStats

class SimpleTable():
    def __init__() -> None:
        pass

    def generateAttemptsTable(memberObjects):
        COL_NAME = 'Name'
        COL_COMP = 'Completion %'
        COL_ATT = 'Att'
        COL_COM = 'Comp'
        outputTable = [[COL_NAME, COL_COMP, COL_ATT, COL_COM]]
        i = 0
        for memberKey in memberObjects:
            memberObject = memberObjects[memberKey]
            # skip empty rows
            if getattr(memberObject, 'totalAttempted') == 0.0:
                continue
            completionPercent = (getattr(memberObject, 'totalCompleted') / getattr(memberObject, 'totalAttempted')) * 100
            outputTable.append(
                [
                    getattr(memberObject, 'displayName'),
                    int(completionPercent),
                    int(getattr(memberObject, 'totalAttempted')),
                    int(getattr(memberObject, 'totalCompleted'))
                ]
            )
        tab = PrettyTable(outputTable[0])
        tab.add_rows(outputTable[1:])
        tab.sortby = 'Completion %'
        tab.reversesort = True
        tab.align[COL_NAME] = 'l'
        tab.align[COL_COMP] = 'r'
        tab.align[COL_ATT] = 'r'
        tab.align[COL_COM] = 'r'
        print(tab)