###############################################################################
# Given an array of MemberStats objects, print various reports
###############################################################################

from prettytable import PrettyTable
from app.MemberStats import MemberStats
from app.LocalController import LocalController
import os

def formatTime(aDuration):
    hours = int(aDuration / 3600)
    minutes = int((aDuration - hours * 3600) / 60)
    seconds = int(aDuration - (hours * 3600) - (minutes * 60))
    return f'{hours:02d}h {minutes:02d}m {seconds:02d}s'


class SimpleTable():
    def __init__() -> None:
        pass


    def generateAttemptsTable(clanName, memberObjects):
        # table column headers
        COL_NAME = 'Name'
        COL_LPER = 'Legend Completion Percent'
        COL_LATT = 'Legend Attempts'
        COL_LCOM = 'Legend Completions'
        COL_NPER = 'Normal Comp %'
        COL_NATT = 'Normal Attempts'
        COL_NCOM = 'Normal Completions'
        COL_PPER = 'Playlist Completion Percent'
        COL_PATT = 'Playlist Attempts'
        COL_PCOM = 'Playlist Completions'
        COL_TPER = 'Total Completion Percent'
        COL_TATT = 'Total Attempts'
        COL_TCOM = 'Total Completions'
        COL_HSPL = 'Maximum Player Score'
        COL_HSTE = 'Maximum Team Score'
        COL_TOPL = 'Total Player Score'
        COL_TOTE = 'Total Team Score'
        COL_TDUR = 'Total Duration'
        COL_TKIL = 'Total Kills'
        COL_TDEA = 'Total Deaths'
        COL_TASS = 'Total Assists'


        # header row
        outputTable = [[COL_NAME,
                        COL_LPER, COL_LCOM, COL_LATT, 
                        COL_NPER, COL_NCOM, COL_NATT, 
                        COL_PPER, COL_PCOM, COL_PATT, 
                        COL_TPER, COL_TCOM, COL_TATT,
                        COL_HSPL, COL_HSTE, COL_TOPL, COL_TOTE,
                        COL_TDUR, COL_TKIL, COL_TDEA, COL_TASS]]
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
            totalPlayerScore = int(getattr(memberObject, 'totalPlayerScore'))
            totalTeamScore = int(getattr(memberObject, 'totalTeamScore'))
            totalDuration = int(getattr(memberObject, 'totalDuration'))
            totalKills = int(getattr(memberObject, 'totalKills'))
            totalDeaths = int(getattr(memberObject, 'totalDeaths'))
            totalAssists = int(getattr(memberObject, 'totalAssists'))


            # build user row
            outputTable.append(
                [
                    getattr(memberObject, 'displayName'),                                   # 0
                    legendPercent, legendTotalCompleted, legendTotalAttempted,              # 1 2 3
                    normalPercent, normalTotalCompleted, normalTotalAttempted,              # 4 5 6
                    playlistPercent, playlistTotalCompleted, playlistTotalAttemtped,        # 7 8 9
                    totalPercent, totalCompleted, totalAttempted,                           # 10 11 12
                    highestPlayerScore, highestTeamScore, totalPlayerScore, totalTeamScore, # 13 14 15
                    formatTime(totalDuration), totalKills, totalDeaths, totalAssists        # 16 17 18 19
                ]
            )

        tab = PrettyTable(outputTable[0])
        tab.add_rows(outputTable[1:])
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
        tab.align[COL_TOPL] = 'r'
        tab.align[COL_TOTE] = 'r'
        tab.align[COL_TDUR] = 'r'
        tab.align[COL_TKIL] = 'r'
        tab.align[COL_TDEA] = 'r'
        tab.align[COL_TASS] = 'r'

        # all stats
        tab.sortby = COL_NAME
        tab.reversesort = False
        reportAllStats = tab.get_string()

        # all completions
        tab.sortby = COL_NAME
        tab.reversesort = False
        reportAllCompletions = tab.get_string(fields=[COL_NAME, COL_LCOM, COL_NCOM, COL_PCOM, COL_TCOM])

        # sort high-to-low (desc)
        tab.reversesort = True

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

        # points
        tab.sortby = COL_HSPL
        playerMaxPoints = tab.get_string(fields=[COL_NAME, COL_HSPL])
        tab.sortby = COL_HSTE
        teamMaxPoints = tab.get_string(fields=[COL_NAME, COL_HSTE])
        tab.sortby = COL_TOPL
        playerTotalPoints = tab.get_string(fields=[COL_NAME, COL_TOPL])
        tab.sortby = COL_TOTE
        teamTotalPoints = tab.get_string(fields=[COL_NAME, COL_TOTE])

        # stats
        tab.sortby = COL_TDUR
        # format duration string AFTER sorting?
        reportTotalDuration = tab.get_string(fields=[COL_NAME, COL_TDUR])
        tab.sortby = COL_TKIL
        reportTotalKills = tab.get_string(fields=[COL_NAME, COL_TKIL])
        tab.sortby = COL_TDEA
        reportTotalDeaths = tab.get_string(fields=[COL_NAME, COL_TDEA])
        tab.sortby = COL_TASS
        reportTotalAssists = tab.get_string(fields=[COL_NAME, COL_TASS])

        reports = {
            COL_LCOM: reportLegendCompletions,
            COL_LATT: reportLegendAttempts,
            COL_LPER: reportLegendPercent,
            COL_NCOM: reportNormalCompletions,
            COL_NATT: reportNormalAttempts,
            COL_NPER: reportNormalPercent,
            COL_PCOM: reportPlaylistCompletions,
            COL_PATT: reportPlaylistAttempts,
            COL_PPER: reportPlaylistPercent,
            COL_TCOM: reportTotalCompletions,
            COL_TATT: reportTotalAttempts,
            COL_TPER: reportTotalPercent,
            COL_HSPL: playerMaxPoints,
            COL_HSTE: teamMaxPoints,
            COL_TOPL: playerTotalPoints,
            COL_TOTE: teamTotalPoints,
            COL_TDUR: reportTotalDuration,
            COL_TKIL: reportTotalKills,
            COL_TDEA: reportTotalDeaths,
            COL_TASS: reportTotalAssists,
            COL_NAME: reportAllCompletions,
            'AllStats': reportAllStats
        }

        resultsFolderPath = LocalController.GetResultDirectory(clanName)
        for keys in reports.keys():
            with open(os.path.join(resultsFolderPath, f'{keys}.txt'), mode='w', encoding='utf-8') as f:
                f.write(reports[keys])
                f.write('\n\n')

        print(reportAllCompletions)
