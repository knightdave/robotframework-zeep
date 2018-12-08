from .ZeepKeywords import ZeepKeywords
from .version import VERSION

_version_ = VERSION


class ZeepLibrary(ZeepKeywords):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'