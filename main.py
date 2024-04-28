from app.Director import Director
from app.ManifestController import DestinyManifest
from app.PgcrCollector import PGCRCollector
from app.bungieapi import BungieApi
from app.ClanCollector import ClanCollector
from app.data.onslaughthash import ONSLAUGHT_ACTIVITIES
from app.MemberStats import MemberStats
from app.report.SimpleTable import SimpleTable

###############################################################################
#
# main()
#
###############################################################################
if __name__ == '__main__':
    import pathos, argparse, os, time
    from tqdm import tqdm

    # build argument parsing
    descriptionString = """Get and compile Onslaught stats for a Destiny 2 clan.
    example: main.py -c 174643"""
    parser = argparse.ArgumentParser(prog='main.py', description=f'{descriptionString}', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--clan', '-c', type=int, required=False, help='Clan ID as reported on Bungie.net', default='174643')
    parser.add_argument('--use-cache', required=False, help='Pull cache data from Bungie API', default=False, action='store_true')
    parser.add_argument('--no-report', required=False, help='Do not generate report data', default=False, action='store_true')
    args = vars(parser.parse_args())
    clan = args['clan']
    freshPull = not args['use_cache']
    generateReport = not args['no_report']

    # Manually set clan ID
    # CLAN_ID = 881267
                                                                                                                                     
    API_KEY = os.getenv('BUNGIE_API_KEY')
    # Manually set API key
    # API_KEY = "123456789"
    
    Director.CreateCacheFolder()

    # check manifest
    manifest = DestinyManifest().update(freshPull)
    api = BungieApi(API_KEY)

    # create clan holder
    cc = ClanCollector(clan, api)
    cc.update(freshPull)
    clanName = cc.getDisplayName()

    # set up results directories
    Director.CreateDirectoriesForClan(clanName)
    Director.ClearResultDirectory(clanName)
    Director.CreateDirectoriesForClan(clanName)

    # populate clan members
    cc.getClanMemberList(freshPull)

    from pathos.multiprocessing import ProcessPool, ThreadPool, ThreadingPool
    pathos.helpers.freeze_support()  # required for windows
    pool = ProcessPool()
    # You could also specify the amount of threads. Note that this DRASTICALLY speeds up the process but takes serious computation power.
    # pool = ProcessPool(40)
    memberObjects = {}
    # populate PGCRs from clan members
    for member in tqdm(cc.getClanMembers(), desc="> Fetching clan member PGCRs"):
        member = member['destinyUserInfo']
        memberPlatform = member['membershipType']
        memberUserId = member['membershipId']
        pc = PGCRCollector(clanName, member, api, pool)
        memberDisplayName = pc.getProfile().getDisplayName()
        Director.CreateDirectoriesForMember(clanName, memberDisplayName)

        if freshPull:
            pc.getCharacters().getActivities(limit=None).getPGCRs()
            #data = pc.getAllPgcrs()
            time.sleep(1.0) # I was getting weird 503 errors without this
    
    if generateReport:
        for member in cc.getClanMembers():
            member = member['destinyUserInfo']
            mb = MemberStats(clanName, member).update()
            memberDisplayName = mb.getDisplayName()
            print(f"> Generate reports for {memberDisplayName}")
            mb.loadPGCRs()
            memberObjects[memberDisplayName] = mb
            mb = None

    
    SimpleTable.generateAttemptsTable(memberObjects)


    pool.close()
