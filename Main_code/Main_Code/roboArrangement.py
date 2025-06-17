import random
import math
from typing import Dict, List, Set, Tuple, Any
from robot import robot
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('robot_arrangement.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# set to hold the working robots
workingBots: Set[str] = set()

# all the bots
allBots: Set[str] = set()

# message bots
messageBots: Set[str] = set()

# mapping the bots with destination to the bot index
botMapping: Dict[str, int] = {}

def createString(data: Dict[str, int]) -> str:
    """Create a string representation of coordinates."""
    return f"{data['x']}-{data['y']}"

def createStringBots(_robot: List[Any]) -> str:
    """Create a string representation of robot coordinates."""
    return f"{_robot[4][0]}-{_robot[4][1]}"

def createTuple(string: str) -> List[int]:
    """Convert coordinate string to tuple."""
    try:
        tmp = string.split('-')
        return [int(tmp[0]), int(tmp[1])]
    except (ValueError, IndexError) as e:
        logger.error(f"Error converting string to tuple: {e}")
        return [0, 0]

def calcDistance(str1: str, str2: str) -> float:
    """Calculate distance between two coordinate strings."""
    try:
        t1 = createTuple(str1)
        t2 = createTuple(str2)
        return math.sqrt((t1[0] - t2[0]) ** 2 + (t1[1] - t2[1]) ** 2)
    except Exception as e:
        logger.error(f"Error calculating distance: {e}")
        return float('inf')

def leastDistBot(idleBots: Set[str], dest: str) -> str:
    """Find the robot closest to the destination."""
    try:
        minDist = float('inf')
        minBot = ''
        for _bot in idleBots:
            distance = calcDistance(_bot, dest)
            if distance < minDist:
                minDist = distance
                minBot = _bot
        return minBot
    except Exception as e:
        logger.error(f"Error finding least distance bot: {e}")
        return ''

def assignBot(listOfDest: List[Dict[str, int]], robotList: Dict[int, List[Any]]) -> None:
    """Assign robots to destinations."""
    global allBots, workingBots, botMapping, messageBots
    try:
        # find the idle bots
        idleBots = allBots - workingBots

        for dest in listOfDest:
            if len(idleBots) == 0:
                logger.warning('No free bots available')
                continue
            
            selectedBot = leastDistBot(idleBots, dest)
            if not selectedBot:
                continue
                
            selBot = robotList[botMapping[selectedBot]]
            selBot[4] = createTuple(createString(dest))  # setting the destination
            selBot[5] = False
            idleBots.remove(selectedBot)
            workingBots.add(createString(dest))
            logger.info(f"Assigned bot {selectedBot} to destination {dest}")
    except Exception as e:
        logger.error(f"Error in assignBot: {e}")

def idleBot(listOfBots: Set[str], robotList: Dict[int, List[Any]]) -> None:
    """Set robots to idle state."""
    global allBots, workingBots, botMapping, messageBots
    try:
        for bot in listOfBots:
            workingBots.remove(bot)
            robotList[botMapping[bot]][5] = True
            logger.info(f"Set bot {bot} to idle")
    except Exception as e:
        logger.error(f"Error in idleBot: {e}")

def arrageBot(robotList: Dict[int, List[Any]], message: List[Dict[str, int]]) -> None:
    """Arrange robots based on message destinations."""
    global allBots, workingBots, botMapping, messageBots
    try:
        allBots = set()
        messageBots = set()
        botMapping = {}

        # loop through the robot list and add to the all robot list
        for key, robot in robotList.items():
            _robot = robotList[key]
            allBots.add(createStringBots(robot))
            botMapping[createStringBots(robot)] = key

        # loop through the list and find the message bots
        for des in message:
            messageBots.add(createString(des))

        # find the bots should be idled
        shouldIdle = workingBots - messageBots

        # should assign
        shouldAssign = messageBots - workingBots

        logger.info(f'All bots: {allBots}')
        logger.info(f'Should idle: {shouldIdle}')
        logger.info(f'Should assign: {shouldAssign}')

        # idling the bots
        idleBot(shouldIdle, robotList)

        # assigning the bots
        assignBot(list(shouldAssign), robotList)
    except Exception as e:
        logger.error(f"Error in arrageBot: {e}")

# BOT_COUNT = 8
# ARENA_DIM = 30
# robots_data = []


# def initialize():
#     global robots_data
#     for i in range(BOT_COUNT):
#         robots_data.append(
#             robot(
#                 # TODO the corner bug should be resolved at the client
#                 (random.randint(5, ARENA_DIM-5), random.randint(5, ARENA_DIM-5)),
#                 0,
#                 (random.randint(5, ARENA_DIM-5), random.randint(5, ARENA_DIM-5)),
#                 0
#             )
#         )

# initialize()
# print(len(robots_data))

# arr = [{'x': 24, 'y': 18}, {'x': 24, 'y': 12}, {'x': 21, 'y': 11},
#        {'x': 27, 'y': 16}, {'x': 22, 'y': 27}, {'x': 28, 'y': 23}]

# arrageBot(robots_data, arr)

# arr = [{'x': 24, 'y': 18}, {'x': 24, 'y': 12}, {'x': 21, 'y': 11},
#        {'x': 27, 'y': 16}, {'x': 22, 'y': 27}, {'x': 28, 'y': 24}]

# arrageBot(robots_data, arr)
# arrageBot(robots_data, arr)
