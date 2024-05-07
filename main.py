from app.LocalController import LocalController
from app.PgcrCollector import PGCRCollector
from app.ApiController import ApiController
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

    NULL_CLAN = 'UserInput'

    # build argument parsing
    descriptionString = """Get and compile Onslaught stats for a Destiny 2 clan or individual user.
        clan example: main.py -c 174643
        user example: main.py -p 3 -id 4611686018472661350"""
    parser = argparse.ArgumentParser(prog='main.py', description=f'{descriptionString}', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--bungie-api-key', '-key', type=str, required=False, help='Your Bungie API key')
    parser.add_argument('--clan', '-c', type=int, required=False, help='Clan ID as reported on Bungie.net', default='174643')
    parser.add_argument('--member', '-m', type=int, required=False, help='User ID as reported on Bungie.net')
    parser.add_argument('--platform', '-p', type=int, required=False, help='Your platform ID as reported on Bungie.net')
    parser.add_argument('--use-cache', required=False, help='Pull cache data instead of Bungie API', default=False, action='store_true')
    parser.add_argument('--no-report', required=False, help='Do not generate report data', default=False, action='store_true')
    args = vars(parser.parse_args())
    API_KEY = args['bungie_api_key']
    clan = args['clan']
    memberId = args['member']
    platform = args['platform']
    freshPull = not args['use_cache']
    generateReport = not args['no_report']

    # Manually set clan ID
    # CLAN_ID = 881267

    # Manually set user ID
    # PLATFORM_ID = 3
    # MEMBER_ID = 4611686018472661350

    if API_KEY == None:
        API_KEY = os.getenv('BUNGIE_API_KEY')
    if API_KEY == None:
        # Manually set API key
        API_KEY = '123456789' 
    
    LocalController.CreateCacheFolder()

    # check manifest
    api = ApiController(api_key=API_KEY, freshPull=freshPull)

    # create clan holder
    if memberId == None:
        cc = ClanCollector(clan, api)
        cc.update(freshPull)
        clanName = cc.getDisplayName()
    else:
        cc = ClanCollector(clanId=0, api=api)
        clanName = NULL_CLAN

    # set up results directories
    LocalController.CreateDirectoriesForClan(clanName)
    LocalController.ClearResultDirectory(clanName)
    LocalController.CreateDirectoriesForClan(clanName)

    # populate clan members
    if memberId == None:
        cc.getClanMemberList(freshPull)
    else:
        cc.addMember(platform=platform, membershipId=memberId)

    from pathos.multiprocessing import ProcessPool, ThreadPool, ThreadingPool
    pathos.helpers.freeze_support()  # required for windows
    pool = ProcessPool()
    # You could also specify the amount of threads. Note that this DRASTICALLY speeds up the process but takes serious computation power.
    # pool = ProcessPool(40)
    memberObjects = {}
    # populate PGCRs from clan members
    if freshPull:
        for member in tqdm(cc.getClanMembers(), desc="> Fetching clan member PGCRs"):
            member = member['destinyUserInfo']
            memberPlatform = member['membershipType']
            memberUserId = member['membershipId']
            pc = PGCRCollector(clanName, member, api, pool)
            memberDisplayName = pc.getProfile().getDisplayName()
            LocalController.CreateDirectoriesForMember(clanName, memberDisplayName)

            pc.getCharacters().getActivities(limit=None).getPGCRs()
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

    SimpleTable.generateAttemptsTable(clanName, memberObjects)

    pool.close()
