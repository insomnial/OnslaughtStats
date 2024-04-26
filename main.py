from app.Director import Director
from app.bungiemanifest import DestinyManifest
from app.PgcrCollector import PGCRCollector
from app.bungieapi import BungieApi
from app.ClanCollector import ClanCollector

###############################################################################
#
# main()
#
###############################################################################
if __name__ == '__main__':
    import pathos, argparse, os

    # build argument parsing
    descriptionString = """Get and compile Onslaught stats for a Destiny 2 clan.
    example: main.py -c 174643"""
    parser = argparse.ArgumentParser(prog='main.py', description=f'{descriptionString}', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--clan', '-c', type=int, required=False, help='Clan ID as reported on Bungie.net')
    args = vars(parser.parse_args())
    clan = args['clan']

    if clan != None:
        CLAN_ID = clan
    else:
        # Manually set clan ID here
        CLAN_ID = 881267

    from pathos.multiprocessing import ProcessPool, ThreadPool, ThreadingPool
    pathos.helpers.freeze_support()  # required for windows
    pool = ProcessPool()
    # You could also specify the amount of threads. Note that this DRASTICALLY speeds up the process but takes serious computation power.
    # pool = ProcessPool(40)
                                                                                                                                             
    # check manifest
    manifest = DestinyManifest().update()

    API_KEY = os.getenv('BUNGIE_API_KEY')
    # Manually set API key
    # API_KEY = "123456789"
    
    api = BungieApi(API_KEY)

    cc = ClanCollector(CLAN_ID, api)
    cc.update()
    clanName = cc.getDisplayName()

    #pc = PGCRCollector(systemPlatform, userId, api, pool)
    #displayName = pc.getProfile().getDisplayName()

    Director.CreateDirectoriesForUser(clanName)
    Director.ClearResultDirectory(clanName)
    Director.CreateDirectoriesForUser(clanName)
    
    #pc.getCharacters().getActivities(limit=None).getPGCRs()  # .combineAllPgcrs()
    #data = pc.getAllPgcrs()

    pool.close()
