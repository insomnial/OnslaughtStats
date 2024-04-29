###############################################################################
#
# Given a user name:
# 1) Initialize user variables
# 2) Find the PGCR folder
# 3) Move through PGCRs and count stats
#
###############################################################################

from app.LocalController import LocalController
from app.data.onslaughthash import ONSLAUGHT_ACTIVITIES

class MemberStats:
    def __init__(self, clanName, member) -> None:
        super().__init__()
        self.clanName = clanName
        self.memberObj = member
        self.displayName = None
        self.memberUserId = None
        self.onslaughtPGCRs = []
        self.totalAttempted = 0
        self.totalCompleted = 0
        self.playlistTotalAttemtped = 0
        self.playlistTotalCompleted = 0
        self.normalTotalAttempted = 0
        self.normalTotalCompleted = 0
        self.legendTotalAttempted = 0
        self.legendTotalCompleted = 0
        self.totalDuration = 0
        self.totalKills = 0
        self.totalDeaths = 0
        self.totalAssists = 0
        self.Playlist = 0                    # 2769402771
        self.MidtownPlaylistAttempted = 0    # 203968370     10-wave playlist
        self.MidtownPlaylistCompleted = 0    # 203968370     10-wave playlist
        self.MidtownNormalAttempted = 0      # 2295195925    50-wave normal
        self.MidtownNormalCompleted = 0      # 2295195925    50-wave normal
        self.MidtownLegendAttempted = 0      # 2064836415    50-wave legend
        self.MidtownLegendCompleted = 0      # 2064836415    50-wave legend
        self.MothyardsPlaylistAttempted = 0  # 2063776142    10-wave playlist
        self.MothyardsPlaylistCompleted = 0  # 2063776142    10-wave playlist
        self.MothyardsNormalAttempted = 0    # 887771978     50-wave normal
        self.MothyardsNormalCompleted = 0    # 887771978     50-wave normal
        self.MothyardsLegendAttempted = 0    # 447898400     50-wave legend
        self.MothyardsLegendCompleted = 0    # 447898400     50-wave legend
        self.VostokPlaylistAttempted = 0     # 1428607109    10-wave playlist
        self.VostokPlaylistCompleted = 0     # 1428607109    10-wave playlist
        self.VostokNormalAttempted = 0       # 3439345485    50-wave normal
        self.VostokNormalCompleted = 0       # 3439345485    50-wave normal
        self.VostokLegendAttempted = 0       # 264092439     50-wave legend
        self.VostokLegendCompleted = 0       # 264092439     50-wave legend
        self.totalPlayerScore = 0            # ['entries']['score']['basic']['value']
        self.totalTeamScore = 0
        self.highestPlayerScore = 0
        self.highestTeamScore = 0


    def update(self):
        self.memberUserId = self.memberObj['membershipId']
        bungieGlobalDisplayName = self.memberUserId
        bungieGlobalDisplayName = self.memberObj['displayName'] # default name
        if 'bungieGlobalDisplayName' in self.memberObj:
            bungieGlobalDisplayName = self.memberObj['bungieGlobalDisplayName']
        bungieGlobalDisplayNameCode = 0
        if 'bungieGlobalDisplayNameCode' in self.memberObj:
            bungieGlobalDisplayNameCode = self.memberObj['bungieGlobalDisplayNameCode']
        self.displayName = f'{bungieGlobalDisplayName}[{bungieGlobalDisplayNameCode:04d}]'
        return self


    def getPGCRDirectory(self):
        return LocalController.GetPGCRDirectoryMember(self.clanName, self.displayName)
    

    def getDisplayName(self):
        return self.displayName


    # process new activity from PGCR
    def loadPGCRs(self):
        import os, json
        from tqdm import tqdm

        pgcrFolder = MemberStats.getPGCRDirectory(self)
        fileList = [f'{pgcrFolder}{f}' for f in os.listdir(pgcrFolder)]
        for filepath in fileList: # go through each file
            with open(f'{filepath}', 'r', encoding='utf-8') as f: # open file and load json
                pgcr = json.load(f)

            if 'skip' in pgcr:  
                continue # skip offensive activities that aren't onslaught
            
            self.onslaughtPGCRs.append(pgcr['activityDetails']['instanceId']) # save this PGCR as an onslaught activity

            onslaughtType = pgcr['activityDetails']['referenceId']

            entries = pgcr['entries']
            # find the player in the entries
            for entry in entries:
                curMembershipId = entry['player']['destinyUserInfo']['membershipId']
                if curMembershipId == self.memberUserId:
                    pgcr = entry['values']
                    
            # get stats
            assists = pgcr['assists']['basic']['value']
            attempted = 1.0
            completed = pgcr['completed']['basic']['value']
            completionReason = pgcr['completionReason']['basic']['value']
            completedReasonValue = 1.0 if completionReason == 0.0 else 0.0
            deaths = pgcr['deaths']['basic']['value']
            kills = pgcr['kills']['basic']['value']
            playerScore = pgcr['score']['basic']['value']
            duration = pgcr['activityDurationSeconds']['basic']['value']
            teamScore = pgcr['teamScore']['basic']['value']

            # process stats
            self.totalAttempted += attempted
            self.totalCompleted += completedReasonValue
            self.highestPlayerScore = playerScore if playerScore > self.highestPlayerScore else self.highestPlayerScore
            self.highestTeamScore = teamScore if teamScore > self.highestTeamScore else self.highestTeamScore
            self.totalPlayerScore += playerScore
            self.totalTeamScore += teamScore
            self.totalDuration += duration
            self.totalKills += kills
            self.totalDeaths += deaths
            self.totalAssists += assists

            match onslaughtType:
                case 203968370: #'Midtown'
                    self.MidtownPlaylistAttempted += attempted
                    self.MidtownPlaylistCompleted += completedReasonValue
                    self.playlistTotalAttemtped += attempted
                    self.playlistTotalCompleted += completedReasonValue
                case 2295195925: #'Midtown: Onslaught'
                    self.MidtownNormalAttempted += attempted
                    self.MidtownNormalCompleted += completedReasonValue
                    self.normalTotalAttempted += attempted
                    self.normalTotalCompleted += completedReasonValue
                case 2064836415: #'Legend: Midtown: Onslaught'
                    self.MidtownLegendAttempted += attempted
                    self.MidtownLegendCompleted += completedReasonValue
                    self.legendTotalAttempted += attempted
                    self.legendTotalCompleted += completedReasonValue
                case 2063776142: #'Mothyards'
                    self.MothyardsPlaylistAttempted += attempted
                    self.MothyardsPlaylistCompleted += completedReasonValue
                    self.playlistTotalAttemtped += attempted
                    self.playlistTotalCompleted += completedReasonValue
                case 887771978: #'Mothyards: Onslaught'
                    self.MothyardsNormalAttempted += attempted
                    self.MothyardsNormalCompleted += completedReasonValue
                    self.normalTotalAttempted += attempted
                    self.normalTotalCompleted += completedReasonValue
                case 447898400: #'Legend: Mothyards: Onslaught'
                    self.MothyardsLegendAttempted += attempted
                    self.MothyardsLegendCompleted += completedReasonValue
                    self.legendTotalAttempted += attempted
                    self.legendTotalCompleted += completedReasonValue
                case 1428607109: #'Vostok'
                    self.VostokPlaylistAttempted += attempted
                    self.VostokPlaylistCompleted += completedReasonValue
                    self.playlistTotalAttemtped += attempted
                    self.playlistTotalCompleted += completedReasonValue
                case 3439345485: #'Vostok: Onslaught'
                    self.VostokNormalAttempted += attempted
                    self.VostokNormalCompleted += completedReasonValue
                    self.normalTotalAttempted += attempted
                    self.normalTotalCompleted += completedReasonValue
                case 264092439: #'Legend: Vostok: Onslaught
                    self.VostokLegendAttempted += attempted
                    self.VostokLegendCompleted += completedReasonValue
                    self.legendTotalAttempted += attempted
                    self.legendTotalCompleted += completedReasonValue
                case _:
                    print(f'Unknown PGCR activity {filepath}')

        return self        