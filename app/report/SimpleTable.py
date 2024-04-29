###############################################################################
# Given an array of MemberStats objects, print various reports
###############################################################################

from prettytable import PrettyTable
from app.MemberStats import MemberStats
from app.LocalController import LocalController
import os

class SimpleTable():
    def __init__() -> None:
        pass

    def generateAttemptsTable(clanName, memberObjects):
        # table column headers
        COL_NAME = 'Name'
        COL_LPER = 'Leg Comp %'
        COL_LATT = 'Leg Att'
        COL_LCOM = 'Leg Comp'
        COL_NPER = 'Nor Comp %'
        COL_NATT = 'Nor Att'
        COL_NCOM = 'Nor Com'
        COL_PPER = 'Pla Comp %'
        COL_PATT = 'Pla Att'
        COL_PCOM = 'Pla Com'
        COL_TPER = 'Tot Comp %'
        COL_TATT = 'Tot Att'
        COL_TCOM = 'Tot Comp'
        COL_HSPL = 'Max Ply'
        COL_HSTE = 'Max Tea'
        # header row
        outputTable = [[COL_NAME,
                        COL_LPER, COL_LCOM, COL_LATT, 
                        COL_NPER, COL_NCOM, COL_NATT, 
                        COL_PPER, COL_PCOM, COL_PATT, 
                        COL_TPER, COL_TCOM, COL_TATT,
                        COL_HSPL, COL_HSTE]]
        # get user data
        for memberKey in memberObjects:
            memberObject = memberObjects[memberKey]
            # skip empty data sets
            if getattr(memberObject, 'totalAttempted') == 0.0:
                continue
            # build stats
            legendTotalAttempted = int(getattr(memberObject, 'legendTotalAttempted'))
            legendTotalCompleted = int(getattr(memberObject, 'legendTotalCompleted'))
            legendPercent = int(0 if legendTotalCompleted == 0 else int((legendTotalCompleted / legendTotalAttempted) * 100))
            normalTotalAttempted = int(getattr(memberObject, 'normalTotalAttempted'))
            normalTotalCompleted = int(getattr(memberObject, 'normalTotalCompleted'))
            normalPercent = int(0 if normalTotalCompleted == 0 else (normalTotalCompleted / normalTotalAttempted) * 100)
            playlistTotalAttemtped = int(getattr(memberObject, 'playlistTotalAttemtped'))
            playlistTotalCompleted = int(getattr(memberObject, 'playlistTotalCompleted'))
            playlistPercent = int(0 if playlistTotalCompleted == 0 else (playlistTotalCompleted / playlistTotalAttemtped) * 100)
            totalAttempted = int(getattr(memberObject, 'totalAttempted'))
            totalCompleted = int(getattr(memberObject, 'totalCompleted'))
            totalPercent = int(0 if totalCompleted == 0 else (totalCompleted / totalAttempted) * 100)
            highestPlayerScore = int(getattr(memberObject, 'highestPlayerScore'))
            highestTeamScore = int(getattr(memberObject, 'highestTeamScore'))

            # build user row
            outputTable.append(
                [
                    getattr(memberObject, 'displayName'),
                    legendPercent, legendTotalCompleted, legendTotalAttempted,
                    normalPercent, normalTotalCompleted, normalTotalAttempted,
                    playlistPercent, playlistTotalCompleted, playlistTotalAttemtped,
                    totalPercent, totalCompleted, totalAttempted,
                    highestPlayerScore, highestTeamScore
                ]
            )

        tab = PrettyTable(outputTable[0])
        tab.add_rows(outputTable[1:])
        tab.reversesort = True
        tab.align[COL_NAME] = 'l'
        tab.align[COL_LPER] = 'r'
        tab.align[COL_LATT] = 'r'
        tab.align[COL_LCOM] = 'r'
        tab.align[COL_NPER] = 'r'
        tab.align[COL_NATT] = 'r'
        tab.align[COL_NCOM] = 'r'
        tab.align[COL_PPER] = 'r'
        tab.align[COL_PATT] = 'r'
        tab.align[COL_PCOM] = 'r'
        tab.align[COL_TPER] = 'r'
        tab.align[COL_TATT] = 'r'
        tab.align[COL_TCOM] = 'r'
        tab.align[COL_HSPL] = 'r'
        tab.align[COL_HSTE] = 'r'

        # legend
        tab.sortby = COL_LCOM
        reportLegendCompletions = tab.get_string(fields=[COL_NAME, COL_LCOM])
        tab.sortby = COL_LATT
        reportLegendAttempts = tab.get_string(fields=[COL_NAME, COL_LATT])
        tab.sortby = COL_LPER
        reportLegendPercent = tab.get_string(fields=[COL_NAME, COL_LPER])

        # normal
        tab.sortby = COL_NCOM
        reportNormalCompletions = tab.get_string(fields=[COL_NAME, COL_NCOM])
        tab.sortby = COL_NATT
        reportNormalAttempts = tab.get_string(fields=[COL_NAME, COL_NATT])
        tab.sortby = COL_NPER
        reportNormalPercent = tab.get_string(fields=[COL_NAME, COL_NPER])

        # playlist
        tab.sortby = COL_PCOM
        reportPlaylistCompletions = tab.get_string(fields=[COL_NAME, COL_PCOM])
        tab.sortby = COL_PATT
        reportPlaylistAttempts = tab.get_string(fields=[COL_NAME, COL_PATT])
        tab.sortby = COL_PPER
        reportPlaylistPercent = tab.get_string(fields=[COL_NAME, COL_PPER])

        # total
        tab.sortby = COL_TCOM
        reportTotalCompletions = tab.get_string(fields=[COL_NAME, COL_TCOM])
        tab.sortby = COL_TATT
        reportTotalAttempts = tab.get_string(fields=[COL_NAME, COL_TATT])
        tab.sortby = COL_TPER
        reportTotalPercent = tab.get_string(fields=[COL_NAME, COL_TPER])

        #points
        tab.sortby = COL_HSPL
        playerPoints = tab.get_string(fields=[COL_NAME, COL_HSPL])
        tab.sortby = COL_HSTE
        teamPoints = tab.get_string(fields=[COL_NAME, COL_HSTE])

        reports = [
            reportLegendCompletions,
            reportLegendAttempts,
            reportLegendPercent,
            reportNormalCompletions,
            reportNormalAttempts,
            reportNormalPercent,
            reportPlaylistCompletions,
            reportPlaylistAttempts,
            reportPlaylistPercent,
            reportTotalCompletions,
            reportTotalAttempts,
            reportTotalPercent,
            playerPoints,
            teamPoints
        ]

        resultsFolderPath = LocalController.GetResultDirectory(clanName)
        with open(os.path.join(resultsFolderPath, f'{clanName}.txt'), mode='w', encoding='utf-8') as f:
            for report in reports:
                f.write(report)
                f.write('\n\n')

        print(reportTotalPercent)
