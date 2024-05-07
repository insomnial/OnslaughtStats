from typing import Dict
from app.data.classhash import CLASS_HASH
from app.data.activities import ACTIVITY_NAMES
from app.LocalController import LocalController
import requests, os, json

API_ROOT_PATH = 'https://www.bungie.net/Platform'
BUNGIE_BASE = 'https://www.bungie.net'

###############################################################################
# 
# Everything API related
# 
# 
###############################################################################
class ApiController:
    __HEADERS: Dict[str, str]

    ###########################################################################
    # General API functions
    ###########################################################################
    def __init__(self, api_key: str, freshPull = False):
        self.__HEADERS = {'X-API-Key': api_key}
        self.VersionNumber = self.GetVersionNumber(freshPull)
        self.ActivityTypeNames = ACTIVITY_NAMES
        self.ClassHash = CLASS_HASH
        pass

    def GetVersionNumber(self, freshPull):
        if not freshPull:
            print(f"> version check, freshPull = {freshPull}")
            return

        print("> Check version number")
        # get version from manifest file
        manifestPaths = self.wrapAPICall(apiString=f'{API_ROOT_PATH}/Destiny2/Manifest/')
        version = manifestPaths['version']

        # if version file exists and matches response, continue
        if os.path.exists(os.path.join(LocalController.GetCacheRoot(), version)):
            print("Version check passed")
            return

        # if version file does not exist or does not match
        print("Version check failed, deleting cache")
        # delete existing cache folder
        LocalController.DeleteCacheFolder()
        print("Updating version")
        versionFilePath = os.path.join(LocalController.GetCacheRoot(), version)
        # create new version file
        with open(file=versionFilePath, mode='w', encoding='utf-8') as f:
            f.write(version)


    def SaveToCache(aDefinition, aJsonBlob):
        # set root path
        filePath = os.path.join(LocalController.GetCacheRoot(), aDefinition)
        with open(file=filePath, mode='w', encoding='utf-8') as f:
            json.dump(aJsonBlob, f, ensure_ascii=False, indent=4)


    def LoadFromCache(aDefinition):
        filePath = os.path.join(LocalController.GetCacheRoot(), aDefinition)
        exists = os.path.exists(filePath)
        if not exists:
            return None, False
        with open(file=filePath, mode='r', encoding='utf-8') as f:
            blob = json.load(f)
        return blob, True


    def wrapAPICall(self, apiString: str, params = None, timeout = None):
        import time
        for i in range(0, 3):
            call = requests.get(apiString, headers=self.__HEADERS, params=params, timeout=timeout)
            # if params != None and timeout != None:
            #     call = requests.get(apiString, headers=self.__HEADERS, params=params, timeout=timeout)
            # elif params != None and timeout == None:
            #     call = requests.get(apiString, headers=self.__HEADERS, params=params)
            # else:
            #     call = requests.get(apiString, headers=self.__HEADERS)

            # break if it has no error
            if call.status_code // 100 == 2:
                return (call.json())['Response']
            
            errorJson = json.loads(call.text)
            if 'ErrorCode' in errorJson:
                errorCode = errorJson['ErrorCode']
                if errorCode == 1665: # privacy settings enabled for user
                    return errorJson
            
            # wait and try again
            DELAY = 5
            print(f"Attemp {i + 1} failed. Error: {call.status_code}. Waiting {DELAY} seconds and trying again.")
            time.sleep(DELAY)
        print(f"API calls failed. Exiting...")
        exit(2)

    ###########################################################################
    # Specific functions
    ###########################################################################
    def getClanProfile(self, clanId):
        return self.wrapAPICall(f'{API_ROOT_PATH}/GroupV2/{clanId}/')


    def getClanMembers(self, clanId):
        return self.wrapAPICall(f'{API_ROOT_PATH}/GroupV2/{clanId}/Members/')


    def getProfile(self, membershipType, destinyMembershipId, components=[100]):
        params = {}
        if components is not None: params["components"] = components

        return self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}', params=params)


    def getAccountStats(self, membershipType, destinyMembershipId):
        params = {}

        return self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats', params=params)


    def getActivities(self, membershipType, destinyMembershipId, characterId, page=0, count=250, mode=None):
        params = {}
        if page is not None: params["page"] = page
        if count is not None: params["count"] = count
        if mode is not None: params["mode"] = mode

        return self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', params=params)


    def getPGCR(self, activityId):
        params = {}

        return self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/Stats/PostGameCarnageReport/{activityId}/', params=params, timeout=(10, 10))


    def getItem(self, itemReferenceId):
        pass


    def getCharacterStats(self, membershipType, destinyMembershipId, characterId):
        # character:{} 2 keys
        #     data:{
        #         classHash
        #     } 22 keys
        #     privacy:1 // enum ComponentPrivacySetting "Public"

        from app.data.classhash import CLASS_HASH

        params = {}
        params['components'] = 200

        responseJson = (self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}', params=params, timeout=(10, 10)))['character']
        classHash = responseJson['data']['classHash']
        privacy = responseJson['privacy']
        return CLASS_HASH[classHash], privacy
