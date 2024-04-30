from typing import Dict
import requests
from app.data.classhash import CLASS_HASH

API_ROOT_PATH = "https://www.bungie.net/Platform"

class ApiController:
    __HEADERS: Dict[str, str]

    def __init__(self, api_key: str):
        self.__HEADERS = {"X-API-Key": api_key}
        pass


    def wrapAPICall(self, apiString = None, params = None, timeout = None):
        import time
        for i in range(0, 3):
            if params != None and timeout != None:
                call = requests.get(apiString, headers=self.__HEADERS, params=params, timeout=timeout)
            elif params != None and timeout == None:
                call = requests.get(apiString, headers=self.__HEADERS, params=params)
            else:
                call = requests.get(apiString, headers=self.__HEADERS)

            # break if it has no error
            if call.status_code // 100 == 2:
                return (call.json())['Response']
            
            # wait and try again
            print(f"Attemp {i} failed. Error: {call.status_code}. Waiting three seconds and trying again.")
            time.sleep(3)
        print(f"API calls failed. Exiting...")
        exit(2)


    def getClanProfile(self, clanId):
        return self.wrapAPICall(f'{API_ROOT_PATH}/GroupV2/{clanId}/')
    

    def getClanMembers(self, clanId):
        api_call = requests.get(f'{API_ROOT_PATH}/GroupV2/{clanId}/Members/', headers=self.__HEADERS)
        ApiController.checkResponse(api_call.status_code)
        return (api_call.json())['Response']


    def getProfile(self, membershipType, destinyMembershipId, components=[100]):
        params = {}
        if components is not None: params["components"] = components

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}', headers=self.__HEADERS, params=params)
        ApiController.checkResponse(api_call.status_code)

        return (api_call.json())['Response']


    def getAccountStats(self, membershipType, destinyMembershipId):
        params = {}

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Stats', headers=self.__HEADERS, params=params)
        ApiController.checkResponse(api_call.status_code)
        return (api_call.json())['Response']


    def getActivities(self, membershipType, destinyMembershipId, characterId, page=0, count=250, mode=None):
        params = {}
        if page is not None: params["page"] = page
        if count is not None: params["count"] = count
        if mode is not None: params["mode"] = mode

        api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Account/{destinyMembershipId}/Character/{characterId}/Stats/Activities/', headers=self.__HEADERS, params=params)
        ApiController.checkResponse(api_call.status_code)
        json_ = (api_call.json())
        if ("Response" not in json_):
            print(json_)
        return json_['Response']


    def getPGCR(self, activityId):
        params = {}

        try:
            api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/Stats/PostGameCarnageReport/{activityId}/', headers=self.__HEADERS, params=params, timeout=(10, 10))
        except:
            return None
        ApiController.checkResponse(api_call.status_code)
        return (api_call.json())['Response']


    def getItem(self, itemReferenceId):
        pass
    

    def getCharacterClass(self, membershipType, destinyMembershipId, characterId):
        params = {}
        params['components'] = 200

        try:
            api_call = requests.get(f'{API_ROOT_PATH}/Destiny2/{membershipType}/Profile/{destinyMembershipId}/Character/{characterId}', headers=self.__HEADERS, params=params, timeout=(10, 10))
        except:
            return None
        
        ApiController.checkResponse(api_call.status_code)
        classHash = (api_call.json())['Response']['character']['data']['classHash']
        return CLASS_HASH[classHash]
    