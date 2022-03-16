
KEY = 'TOKEN'
ICON = 'https://i.imgur.com/nEatfh9.png'
path = 'PATH' # user double back slashes if on windows, singles for mac. p.s: the folder of downfall, not lapsus. eg: 'C:\\coding\\lapsus\\downfall'

class Channel:
    REVIEWING = 10101010101010101
    REVIEWS = 10101010101010101
    JOINS = 10101010101010101
    COMMANDS = 10101010101010101
    ROSTER = 10101010101010101

    ALLOWED = [COMMANDS]

class Role:
    FAN = 10101010101010101
    TRIAL = 10101010101010101
    MEMBER = 10101010101010101
    MEMBERPLUS = 10101010101010101
    MOD = 10101010101010101

    LEVELS = [None, TRIAL, MEMBER, MEMBERPLUS]

class Guild:
    ID = 10101010101010101

class Color:
    MAIN = 0x663399
    ERROR = 0xC71585