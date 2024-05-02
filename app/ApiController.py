from typing import Dict
import requests

API_ROOT_PATH = "https://www.bungie.net/Platform"

class ApiController:
    __HEADERS: Dict[str, str]

    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key}
        pass


    def wrapAPICall(self, apiString = None, params = None, timeout = None):
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
            
            # TODO something else if the current player is in secret squirrel mode
            
            # wait and try again
            DELAY = 5
            print(f"Attemp {i + 1} failed. Error: {call.status_code}. Waiting {DELAY} seconds and trying again.")
            time.sleep(DELAY)
        print(f"API calls failed. Exiting...")
        exit(2)


    def getClanProfile(self, clanId):
        return self.wrapAPICall(f'{API_ROOT_PATH}/GroupV2/{clanId}/')
    

    def getClanMembers(self, clanId):
        return self.wrapAPICall(f'{API_ROOT_PATH}/GroupV2/{clanId}/Members/')


    def getProfile(self, membershipType, destinyMembershipId, components=[100]):
        params = {}
        if components is not None: params["components"] = components

        return self.wrapAPICall('{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}', params=params)


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
    

    def getCharacterClass(self, membershipType, destinyMembershipId, characterId):
        from app.data.classhash import CLASS_HASH

        params = {}
        params['components'] = 200

        classHash = (self.wrapAPICall(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}', params=params, timeout=(10, 10)))['character']['data']['classHash']
        return CLASS_HASH[classHash]
