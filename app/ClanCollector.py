import os
from itertools import zip_longest

from app.LocalController import LocalController
from app.ApiController import ApiController
import json

from app.internal_timer import Timer


class ClanCollector:
    def __init__(self, clanId, api: ApiController) -> None:
        super().__init__()
        self.api = api
        #save these to cache
        self.clanId = clanId
        self.displayName = None
        self.clanMemberCount = None
        self.clanMemberList = None

        self.members = None


    def generateClanFolders(self):
        # set up results directories
        LocalController.CreateDirectoriesForClan(self.displayName)
        LocalController.ClearResultDirectory(self.displayName)
        LocalController.CreateDirectoriesForClan(self.displayName)

    
    def update(self, freshPull):
        if freshPull:
            print(f"> Get clan profile")
            clanResults = self.api.getClanProfile(self.clanId)
            self.displayName = clanResults['detail']['name']
            self.clanMemberCount = clanResults['detail']['memberCount']
            # save clan information in cache
            self.SaveClanToCache()
            print(f"Found clan: {self.displayName}")
        else:
            print(f"> Get clan profile from cache")
            self.RestoreClanFromCache()
            print(f"Restored clan from cache")
        self.generateClanFolders()
        return self
    

    def SaveClanToCache(self):
        # saves the clan id, name, and member list to a cache file
        clanCache = {}
        clanCache['clanId'] = self.clanId
        clanCache['displayName'] = self.displayName
        clanCache['clanMemberCount'] = self.clanMemberCount
        clanCache['clanMemberList'] = self.clanMemberList
        cacheRoot = LocalController.GetCacheRoot()
        clanFilePath = os.path.join(cacheRoot, str(self.clanId))
        with open(file=clanFilePath, mode='w', encoding='utf-8') as f:
            json.dump(obj=clanCache, fp=f)
            

    def RestoreClanFromCache(self):
        # restores a clan object from a cache file
        cacheRoot = LocalController.GetCacheRoot()
        clanFilePath = os.path.join(cacheRoot, str(self.clanId))
        try:
            with open(file=clanFilePath, mode='r', encoding='utf-8') as f:
                clanCache = json.load(f)
        except:
            print(f"> Failed to find clan in cache: {self.clanId}")
            exit(2)
        self.displayName = clanCache['displayName']
        self.clanMemberCount = clanCache['clanMemberCount']
        self.clanMemberList = clanCache['clanMemberList']


    def getDisplayName(self):
        return self.displayName
    

    def getClanMemberList(self, freshPull):
        if freshPull:
            print(f"> Get clan members")
            self.clanMemberList = (self.api.getClanMembers(self.clanId))['results']
            # save to cache
            self.SaveClanToCache()
            print(f"Found {self.clanMemberCount} members")
        else:
            print("> Get clan members from cache")
            return self
        return self
    
    
    def getClanMembers(self):
        return self.clanMemberList
    

    def addMember(self, platform, membershipId):
        profileJson = (self.api.getProfile(membershipType=platform, destinyMembershipId=membershipId))['profile']['data']['userInfo']
        self.clanMemberList = [{
            'memberType': platform,
            'destinyUserInfo': {
				'membershipType': platform,
				'membershipId': f'{membershipId}',
				'displayName': profileJson['displayName'],
				'bungieGlobalDisplayName': profileJson['bungieGlobalDisplayName'],
				'bungieGlobalDisplayNameCode': profileJson['bungieGlobalDisplayNameCode']
            }}]
        # adding just one member means this is a single user pull, change clan name to reflect that and reset destination folder
        self.displayName = f'{profileJson['bungieGlobalDisplayName']}[{profileJson['bungieGlobalDisplayNameCode']}]'
        self.generateClanFolders()


    def getActivities(self, limit=None):
        print("> Get Activities")
        assert self.characters is not None
        assert len(self.characters) > 0

        existingPgcrList = [f[5:-5] for f in os.listdir(LocalController.GetPGCRDirectoryRoot(self.displayName))]

        self.activities = []
        for k, char_id in enumerate(self.characters):
            page = 0

            def downloadActivityPage(page):
                act = self.api.getActivities(self.membershipType, self.membershipId, char_id, page=page)
                if "activities" not in act:
                    return None
                return [e["activityDetails"]["instanceId"] for e in act["activities"] if e["activityDetails"]["instanceId"] not in existingPgcrList]

            while True:
                steps = 20
                print(k + 1, "/", len(self.characters), "|", char_id, "|", "pages", page + 1, "to", page + steps)
                activityGroups = self.processPool.amap(downloadActivityPage, range(page, page + steps)).get()
                realList = [e for e in activityGroups if e is not None]
                hasNull = len(realList) != steps
                for activityList in realList:
                    self.activities += activityList

                page += steps
                if hasNull:
                    break

                if limit is not None:
                    if len(self.activities) > limit:
                        break

            if limit is not None:
                if len(self.activities) > limit:
                    break
        print("Got ", len(self.activities), " activities that must be downloaded.")

        return self


    def getPGCRs(self):
        bungo = self.api

        def downloadPGCR(activity):
            id = activity
            tries = 0

            pgcr = None
            while pgcr == None and tries < 10:
                tries += 1
                pgcr = bungo.getPGCR(id)

            with open("%s/pgcr_%s.json" % (LocalController.GetPGCRDirectoryRoot(self.displayName), pgcr["activityDetails"]["instanceId"]), "w", encoding='utf-8') as f:
                f.write(json.dumps(pgcr))

        if len(self.activities) == 0:
            print("No activities to grab")
            return self

        from tqdm.auto import tqdm   
        list(tqdm(self.processPool.imap(downloadPGCR, self.activities), total=len(self.activities), desc="Downloading PGCRs"))
        return self


    def combineAllPgcrs(self):
        all = self.getAllPgcrs()
        with Timer("Write all PGCRs to one file"):
            with open(LocalController.GetAllPgcrFilename(self.displayName), "w", encoding='utf-8') as f:
                json.dump(all, f, ensure_ascii=False)
        return self


    def getAllPgcrs(self):

        def loadJson(fnameList):
            r = []
            for fname in fnameList:
                if fname is None:
                    continue
                with open(fname, "r", encoding='utf-8') as f:
                    try:
                        r.append(json.load(f))
                    except Exception:
                        print('Error on %s' % fname)
            return r

        with Timer("Get all PGCRs from individual files"):
            root = LocalController.GetPGCRDirectoryRoot(self.displayName)
            fileList = ["%s/%s" % (root, f) for f in os.listdir(root)]
            chunks = list(zip_longest(*[iter(fileList)] * 100, fillvalue=None))
            pgcrs = self.processPool.amap(loadJson, chunks).get()
            all = [item for sublist in pgcrs for item in sublist]
        return all
