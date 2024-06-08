import json
import os

class PathsManagerException(Exception):
    pass

class PathsManagerInvalidPathException(PathsManagerException):
    def __init__(self, msg: str, path: str):
        super().__init__(msg)
        self.path = path

class PathsManagerInvalidFileException(PathsManagerException):
    def __init__(self, msg):
        super().__init__(msg)

class PathsManagerInvalidArgumentException(PathsManagerException):
    def __init__(self, msg, argument_given, argument_expected):
        super().__init__(msg)
        self.argument_given = argument_given
        self.argument_expected = argument_expected

class PathsManager:
    SUPER_ID = [
        "Rotor",
        "Reflector"
    ]
    ID = [
        "Rotor.json",
        "Reflector.json"
    ]

    def __init__(self):
        self.path = "./paths.json"
        # checking if the file exists
        if not os.path.isfile(self.path):
            raise PathsManagerInvalidPathException("The standard path of the paths.json is wrong."
                                                  " Please make sure all files are there where they should be!", self.path)

    def getPath(self, super_id: int, id: int) -> str:
        """
            This methode returns the searched path via a super_id and an id.
            The super_id marks the upper layer / module to which the path belongs.
            The id in turn defines the specific path which is searched.
            Both Parameter must be indices of their respective lists PathsManager.SUPER_ID and PathsManager.ID.
        """
        # Argument validation
        if super_id < 0 or super_id >= len(PathsManager.SUPER_ID):
            raise PathsManagerInvalidArgumentException("The super_id needs to be in the indices of the list "
                                                       "PathsManager.SUPER_ID",
                                                       super_id, range(len(PathsManager.SUPER_ID)))
        if id < 0 or id >= len(PathsManager.ID):
            raise PathsManagerInvalidArgumentException("The id needs to be in the indices of the list PathsManager.ID",
                                                       id, range(len(PathsManager.ID)))

        # opening and validating json
        with open(self.path, "r") as js:
            paths = json.load(js)
        if paths is None or len(paths) == 0:
            raise PathsManagerInvalidFileException("The paths.json file is empty!")

        # returns the correct path
        return paths[PathsManager.SUPER_ID[super_id]][PathsManager.ID[id]]