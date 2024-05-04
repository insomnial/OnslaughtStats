import shutil
from pathlib import Path


class LocalController:

    @staticmethod
    def ClearResultDirectory(clanName):
        path = LocalController.GetResultDirectory(clanName)
        shutil.rmtree(path)

    @staticmethod
    def GetResultDirectory(clanName):
        return f'./data/{clanName}/result/'

    @staticmethod
    def GetPGCRDirectoryRoot(clanName):
        return f'./data/{clanName}/pgcr/'
    
    @staticmethod
    def GetPGCRDirectoryMember(clanName, memberName):
        return f'./data/{clanName}/pgcr/{memberName}/'

    @staticmethod
    def GetAllPgcrFilename(clanName):
        return f'./data/{clanName}/pgcr.json'
    
    @staticmethod
    def GetCacheRoot():
        return './cache/'
    
    @staticmethod
    def CreateDirectoriesForClan(clanName):
        Path(LocalController.GetResultDirectory(clanName)).mkdir(parents=True, exist_ok=True)
        Path(LocalController.GetPGCRDirectoryRoot(clanName)).mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def CreateDirectoriesForMember(clanName, memberName):
        Path(LocalController.GetPGCRDirectoryMember(clanName, memberName)).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def CreateCacheFolder():
        Path(LocalController.GetCacheRoot()).mkdir(parents=True, exist_ok=True)

    @staticmethod
    def DeleteCacheFolder():
        shutil.rmtree(LocalController.GetCacheRoot(), ignore_errors=True)
        LocalController.CreateCacheFolder()

        