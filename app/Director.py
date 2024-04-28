import shutil
from pathlib import Path


class Director:

    @staticmethod
    def ClearResultDirectory(clanName):
        path = Director.GetResultDirectory(clanName)
        shutil.rmtree(path)

    @staticmethod
    def GetResultDirectory(clanName):
        return f"./data/{clanName}/result/"

    @staticmethod
    def GetPGCRDirectoryRoot(clanName):
        return f"./data/{clanName}/pgcr/"
    
    @staticmethod
    def GetPGCRDirectoryMember(clanName, memberName):
        return f"./data/{clanName}/pgcr/{memberName}/"

    @staticmethod
    def GetAllPgcrFilename(clanName):
        return f"./data/{clanName}/pgcr.json"
    
    @staticmethod
    def GetCacheRoot():
        return f"./cache/"
    
    @staticmethod
    def CreateDirectoriesForClan(clanName):
        Path(Director.GetResultDirectory(clanName)).mkdir(parents=True, exist_ok=True)
        Path(Director.GetPGCRDirectoryRoot(clanName)).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def CreateDirectoriesForMember(clanName, memberName):
        Path(Director.GetPGCRDirectoryMember(clanName, memberName)).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def CreateCacheFolder():
        Path(Director.GetCacheRoot()).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def DeleteCacheFolder():
        shutil.rmtree(Director.GetCacheRoot(), ignore_errors=True)

        