# import libraries
import random

# helper functions for creating dictionaries
def add_alley(d):
    """ Allows user to add alley locations to a given dictionary.
        Returns the dictionary when finished. 
    """
    for i in range(1, 190):
        ALLEY_LIST = []      
        stop = 0
        while stop == 0:
            in_a = str(input(f'alleys adjacent to {i}: '))
            in_a = str.upper(in_a)
            print(in_a)
            if in_a == 'N':
                stop = 1
                break
            elif in_a == 'P':
                return d
            else:
                print(f"{in_a} is adjacent to {i}")
                ALLEY_LIST += [in_a]
        print(f"[{i}]['alleys'] == {ALLEY_LIST}")
        d[i]['alleys'] = ALLEY_LIST
    return d

def add_adj_sq(d):
    """Allows the user to add adjacent squares to a given dictionary.
       Returns the dictionary when finished.
    """
    while 1:
        current_square = str(input(f'square name: '))
        current_square = str.upper(current_square)
        d[current_square] = {}
        stop = 0
        SQUARE_LIST = []
        while stop == 0:
            in_s = str(input(f'square adjacent to square {current_square}: '))
            in_s = str.upper(in_s)
            if in_s == 'N':
                stop = 1
                break
            elif in_s == 'P':
                return d
            else:
                print(f"{current_square} is adjacent to {in_s}")
                SQUARE_LIST += [in_s]
        print(f"[{current_square}]['adj squares'] == [{SQUARE_LIST}]")
        d[current_square]['adj squares'] = SQUARE_LIST
    return d

def add_adj_circles(d):
    """Allows the user to add adjacent circles to the given dictionary.
       Returns dictionary when finished.
    """
    SQUARE_LIST = list(d.keys())
    for square in SQUARE_LIST:
        if d[square].get('adj circles') == None:
            stop = 0
            CIRCLE_LIST = []
            while stop == 0:
                in_c = int(input(f'circle adjacent to square {square}: '))
                if in_c == 300:
                    stop = 1
                    break
                elif in_c == 400:
                    return d
                else:
                    print(f"{square} is adjacent to {in_c}")
                    CIRCLE_LIST += [in_c]
            print(f"[{square}]['adj circles'] == [{CIRCLE_LIST}]")
            d[square]['adj circles'] = CIRCLE_LIST
        else:
            print(f"entry {square} complete")
    return d

# Helper function for creating necessary dictionaries
def quads(J):
    """Returns lists of circles in the four quadrants"""
    W1 = dict()
    W2 = dict()
    W3 = dict()
    W4 = dict()
    for i in range(1, 190):
        if J[i]['location'] == 'W1':
            W1.update({i:J[i]})
        elif J[i]['location'] == 'W2':
            W2.update({i:J[i]})
        elif J[i]['location'] == 'W3':
            W3.update({i:J[i]})
        elif J[i]['location'] == 'W4':
            W4.update({i:J[i]})
    return W1, W2, W3, W4

# runGame() runs a game of Whitehall Mystery, providing rule required information for players
# runAdminGame() runs a game while providing helpful information for mainetenance
def runGame():
    """Runs a game of Whitehall Mystery
       Jack moves through AI
       Investigators move through players
    """

    # Gameboard/rules data

    # JACK_DICT contains information relevant to Jack's movements
    # keys correspond to the numbered circles that Jack can occupy
    # 'adjacent': numbered circles adjacent to the key
    # 'location': which part of the board the key is in (white quadrants, black center, or water location)
    # 'alleys': which alleyways the key is adjacent to
    JACK_DICT = {1: {'adjacent': [2, 8, 9, 10, 11, 12, 14, 28, 29], 'location': 'W1', 'alleys': ['ZA']}, 
        2: {'adjacent': [1, 3, 9, 11, 12, 14, 16, 17], 'location': 'W1', 'alleys': ['ZF']}, 
        3: {'adjacent': [2, 4, 16, 17, 18, 19, 20, 21, 37, 38], 'location': 'W1', 'alleys': ['ZG', 'ZH']}, 
        4: {'adjacent': [3, 5, 19, 20, 21, 38], 'location': 'B', 'alleys': ['ZI']}, 
        5: {'adjacent': [4, 20, 22, 23], 'location': 'W2', 'alleys': ['ZJ']}, 
        6: {'adjacent': [23, 24, 25, 45], 'location': 'W2', 'alleys': ['ZM']}, 
        7: {'adjacent': [25, 26, 27, 45], 'location': 'W2', 'alleys': ['ZO']}, 
        8: {'adjacent': [1, 9, 10, 28, 29], 'location': 'W1', 'alleys': [' ']}, 
        9: {'adjacent': [1, 2, 8, 10, 11, 12, 14, 28, 29], 'location': 'W1', 'alleys': ['ZA', 'ZB']}, 
        10: {'adjacent': [1, 8, 9, 11, 13, 28, 29, 30, 31, 32], 'location': 'W1', 'alleys': ['ZB', 'ZS']}, 
        11: {'adjacent': [1, 2, 9, 10, 12, 13, 14, 29, 30, 31, 32], 'location': 'W1', 'alleys': ['ZB', 'ZC']}, 
        12: {'adjacent': [1, 2, 9, 11, 13, 14], 'location': 'W1', 'alleys': ['ZC', 'ZD']}, 
        13: {'adjacent': [10, 11, 12, 14, 15, 16, 29, 30, 31, 32, 33], 'location': 'W1', 'alleys': ['ZC', 'ZE', 'ZT', 'ZU']}, 
        14: {'adjacent': [1, 2, 9, 11, 12, 13, 15, 16], 'location': 'W1', 'alleys': ['ZD', 'ZE', 'ZF']}, 
        15: {'adjacent': [13, 14, 16, 17, 18, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZU', 'ZV']}, 
        16: {'adjacent': [2, 3, 13, 14, 15, 17], 'location': 'W1', 'alleys': ['ZF', 'ZV']}, 
        17: {'adjacent': [2, 3, 15, 16, 18, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZV', 'ZG']}, 
        18: {'adjacent': [3, 15, 17, 19, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZG', 'ZW']}, 
        19: {'adjacent': [3, 4, 18, 20, 21, 37, 38], 'location': 'B', 'alleys': ['ZH', 'ZX']}, 
        20: {'adjacent': [3, 4, 5, 19, 21, 22, 38], 'location': 'B', 'alleys': ['ZI', 'ZJ', 'ZZ']}, 
        21: {'adjacent': [3, 4, 19, 20, 22, 36, 37, 38, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZZ', 'ZY', 'YA']}, 
        22: {'adjacent': [5, 20, 21, 23, 24, 41, 42, 44], 'location': 'B', 'alleys': ['ZJ', 'ZK', 'YA']}, 
        23: {'adjacent': [5, 6, 22, 24, 41, 42, 44], 'location': 'W2', 'alleys': ['ZK', 'ZL']}, 
        24: {'adjacent': [6, 22, 23, 25, 41, 42, 43, 44, 45, 46], 'location': 'W2', 'alleys': ['ZL', 'ZM', 'YD', 'VJ']}, 
        25: {'adjacent': [6, 7, 24, 26, 27, 45], 'location': 'W2', 'alleys': ['ZN', 'ZO']}, 
        26: {'adjacent': [7, 25, 27, 45, 46, 47], 'location': 'W2', 'alleys': ['ZP', 'ZQ', 'YE']}, 
        27: {'adjacent': [7, 25, 26, 45, 47], 'location': 'W2', 'alleys': ['ZQ']}, 
        28: {'adjacent': [1, 8, 9, 10, 29, 30, 48, 49, 50, 51], 'location': 'W1', 'alleys': ['ZR']}, 
        29: {'adjacent': [1, 8, 9, 10, 11, 13, 28, 30, 31, 32], 'location': 'W1', 'alleys': ['ZR', 'ZS']}, 
        30: {'adjacent': [10, 11, 13, 28, 29, 31, 32, 48, 49, 50, 51], 'location': 'W1', 'alleys': ['ZR', 'YH']}, 
        31: {'adjacent': [10, 11, 13, 29, 30, 32, 33, 51, 52, 53], 'location': 'W1', 'alleys': ['YH', 'YI']}, 
        32: {'adjacent': [10, 11, 13, 29, 30, 31, 33, 51, 52, 53], 'location': 'W1', 'alleys': ['YI', 'ZT']}, 
        33: {'adjacent': [13, 15, 17, 18, 31, 32, 34, 35, 37, 51, 52, 53, 54], 'location': 'W1', 'alleys': ['ZT', 'ZU', 'YJ', 'YK']}, 
        34: {'adjacent': [15, 17, 18, 33, 35, 37, 54], 'location': 'W1', 'alleys': ['YK', 'YL']}, 
        35: {'adjacent': [15, 17, 18, 34, 36, 37, 53, 54, 55, 72, 73], 'location': 'W1', 'alleys': ['YL', 'YM']}, 
        36: {'adjacent': [21, 37, 38, 39, 40, 41, 53, 54, 55, 56, 72, 73], 'location': 'W1', 'alleys': ['YM', 'YY']}, 
        37: {'adjacent': [3, 15, 17, 18, 19, 21, 33, 34, 35, 36, 38, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZW', 'ZX', 'YM']}, 
        38: {'adjacent': [3, 4, 19, 20, 21, 36, 37, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZX', 'ZY']}, 
        39: {'adjacent': [21, 36, 37, 38, 40, 41, 42, 56, 57, 58, 59], 'location': 'B', 'alleys': ['YN', 'YO']}, 
        40: {'adjacent': [21, 36, 37, 38, 39, 41, 42, 56, 57, 58, 59], 'location': 'B', 'alleys': ['YB', 'YO']}, 
        41: {'adjacent': [21, 22, 23, 24, 36, 37, 38, 39, 40, 42, 44, 56], 'location': 'B', 'alleys': ['YA', 'YB']}, 
        42: {'adjacent': [22, 23, 24, 39, 40, 41, 43, 44, 56, 57, 58, 59], 'location': 'W2', 'alleys': ['YB', 'ZL', 'YC', 'YP']}, 
        43: {'adjacent': [24, 42, 44, 46, 58, 59, 60, 61, 62, 76, 77, 78], 'location': 'W2', 'alleys': ['YQ', 'YR', 'YS', 'XD']}, 
        44: {'adjacent': [22, 23, 24, 41, 42, 43, 46, 59], 'location': 'W2', 'alleys': ['YC', 'YR', 'VJ']}, 
        45: {'adjacent': [6, 7, 24, 25, 26, 27, 46], 'location': 'W2', 'alleys': ['ZN', 'ZP', 'YD']}, 
        46: {'adjacent': [24, 26, 43, 44, 45, 62, 63, 64, 65, 79, 80, 97], 'location': 'W2', 'alleys': ['YD', 'YS', 'YE', 'XF']}, 
        47: {'adjacent': [26, 27, 65, 67], 'location': 'W2', 'alleys': ['YE']}, 
        48: {'adjacent': [28, 30, 49, 50, 51, 68], 'location': 'W1', 'alleys': ['YG']}, 
        49: {'adjacent': [28, 30, 48, 50, 51, 68], 'location': 'W1', 'alleys': ['YG', 'YT']}, 
        50: {'adjacent': [28, 30, 48, 49, 51, 52, 68, 69, 70], 'location': 'W1', 'alleys': ['YT', 'XG', 'TU']}, 
        51: {'adjacent': [28, 30, 31, 32, 33, 48, 49, 50, 52, 53, 68, 69, 70], 'location': 'W1', 'alleys': ['YH', 'YU', 'YV']}, 
        52: {'adjacent': [31, 32, 33, 50, 51, 53, 55, 68, 69, 70, 71], 'location': 'W1', 'alleys': ['YV', 'YW', 'XJ']}, 
        53: {'adjacent': [31, 32, 33, 35, 36, 51, 52, 54, 55, 72, 73], 'location': 'W1', 'alleys': ['YJ', 'YW']}, 
        54: {'adjacent': [33, 34, 35, 36, 53, 55, 72, 73], 'location': 'W1', 'alleys': ['YJ', 'YL']}, 
        55: {'adjacent': [35, 36, 52, 53, 54, 71, 72, 73, 87], 'location': 'W1', 'alleys': ['YW', 'YX', 'XK']}, 
        56: {'adjacent': [21, 36, 37, 38, 39, 40, 41, 42, 57, 58, 59, 73], 'location': 'B', 'alleys': ['YY', 'YN']}, 
        57: {'adjacent': [39, 40, 42, 56, 58, 59, 73, 74, 75, 76], 'location': 'B', 'alleys': ['YZ', 'XA']}, 
        58: {'adjacent': [39, 40, 42, 43, 56, 57, 59, 60, 73, 74, 75, 76, 77, 78], 'location': 'B', 'alleys': ['XA', 'XB', 'XC']}, 
        59: {'adjacent': [39, 40, 42, 43, 44, 56, 57, 58, 60, 76, 77, 78], 'location': 'B', 'alleys': ['XB', 'YP', 'YQ']}, 
        60: {'adjacent': [43, 58, 59, 61, 62, 76, 77, 78], 'location': 'W2', 'alleys': ['XD', 'XF']}, 
        61: {'adjacent': [43, 60, 62, 63], 'location': 'W2', 'alleys': ['XE', 'XF']}, 
        62: {'adjacent': [43, 46, 60, 61, 63], 'location': 'W2', 'alleys': ['YS', 'XE']}, 
        63: {'adjacent': [46, 61, 62], 'location': 'W2', 'alleys': ['XE', 'XF']}, 
        64: {'adjacent': [46, 65, 66, 67, 79, 80, 97], 'location': 'W2', 'alleys': ['YF']}, 
        65: {'adjacent': [46, 47, 64, 67, 79, 80, 97], 'location': 'W2', 'alleys': ['YE', 'YF']}, 
        66: {'adjacent': [64, 67], 'location': 'H5', 'alleys': [' ']}, 
        67: {'adjacent': [47, 64, 65, 66], 'location': 'W2', 'alleys': ['YF']}, 
        68: {'adjacent': [48, 49, 50, 51, 52, 69, 70, 81, 82, 99], 'location': 'W1', 'alleys': ['XG', 'XH']}, 
        69: {'adjacent': [50, 51, 52, 68, 70, 81, 82, 99], 'location': 'W1', 'alleys': ['XH', 'XI']}, 
        70: {'adjacent': [50, 51, 52, 68, 69, 82, 83, 84, 101], 'location': 'B', 'alleys': ['XI', 'XJ']}, 
        71: {'adjacent': [52, 55, 72, 84, 85, 86, 87], 'location': 'W1', 'alleys': ['XJ', 'XK', 'XL']}, 
        72: {'adjacent': [35, 36, 53, 54, 55, 71, 73, 87], 'location': 'W1', 'alleys': ['YX', 'XM']}, 
        73: {'adjacent': [35, 36, 53, 54, 55, 56, 57, 58, 72, 74, 75, 76], 'location': 'B', 'alleys': ['YY', 'YZ', 'XM']}, 
        74: {'adjacent': [57, 58, 73, 75, 76, 87, 88, 89, 90], 'location': 'B', 'alleys': ['XM', 'XN']}, 
        75: {'adjacent': [57, 58, 73, 74, 76, 77, 87, 88, 89, 90, 92, 93], 'location': 'B', 'alleys': ['XN', 'XO', 'XW']}, 
        76: {'adjacent': [43, 57, 58, 59, 60, 73, 74, 75, 77, 78, 90, 92, 93], 'location': 'B', 'alleys': ['XO', 'XC', 'VK']}, 
        77: {'adjacent': [43, 58, 59, 60, 75, 76, 78, 90, 92, 93], 'location': 'W2', 'alleys': ['VK', 'XP', 'XF']}, 
        78: {'adjacent': [43, 58, 59, 60, 76, 77], 'location': 'W2', 'alleys': ['XP', 'XF']}, 
        79: {'adjacent': [46, 64, 65, 80, 94, 95, 97], 'location': 'W2', 'alleys': ['XF']}, 
        80: {'adjacent': [46, 64, 65, 79, 97], 'location': 'H4', 'alleys': [' ']}, 
        81: {'adjacent': [68, 69, 82, 99, 117, 118], 'location': 'B', 'alleys': ['XQ']}, 
        82: {'adjacent': [68, 69, 70, 81, 83, 84, 99, 101], 'location': 'B', 'alleys': ['XI', 'XR']}, 
        83: {'adjacent': [70, 82, 84, 85, 100, 101, 103], 'location': 'B', 'alleys': ['XS', 'XT']}, 
        84: {'adjacent': [70, 71, 82, 83, 85, 86, 87, 101], 'location': 'B', 'alleys': ['XJ', 'XT']}, 
        85: {'adjacent': [71, 83, 84, 86, 87, 100, 101, 103], 'location': 'B', 'alleys': ['XT', 'WD']}, 
        86: {'adjacent': [71, 84, 85, 87, 88, 89, 105], 'location': 'B', 'alleys': ['XU', 'WD']}, 
        87: {'adjacent': [55, 71, 72, 74, 75, 84, 85, 86, 88, 89, 90], 'location': 'B', 'alleys': ['XU', 'XL', 'XM']}, 
        88: {'adjacent': [74, 75, 86, 87, 89, 90, 105], 'location': 'B', 'alleys': ['XU', 'XV']}, 
        89: {'adjacent': [74, 75, 86, 87, 88, 90, 91, 105, 106, 107, 108], 'location': 'B', 'alleys': ['XV', 'WE', 'XZ', 'WF']}, 
        90: {'adjacent': [74, 75, 76, 77, 87, 88, 89, 91, 92, 93], 'location': 'B', 'alleys': ['XW', 'XX']}, 
        91: {'adjacent': [74, 75, 87, 88, 89, 90, 92, 109], 'location': 'B', 'alleys': ['XX', 'XZ']}, 
        92: {'adjacent': [75, 76, 77, 90, 91, 93, 109], 'location': 'B', 'alleys': ['XX', 'XY']}, 
        93: {'adjacent': [75, 76, 77, 90, 92, 94, 108, 109, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XY', 'XF']}, 
        94: {'adjacent': [79, 93, 95, 108, 109, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XF']}, 
        95: {'adjacent': [79, 94], 'location': 'H4', 'alleys': [' ']}, 
        96: {'adjacent': [97, 98, 113, 114, 115, 116], 'location': 'H4', 'alleys': [' ']}, 
        97: {'adjacent': [46, 64, 65, 79, 80, 96, 98, 113, 114, 115, 116], 'location': 'B', 'alleys': [' ']}, 
        98: {'adjacent': [96, 97, 113, 114, 115, 116], 'location': 'H5', 'alleys': [' ']}, 
        99: {'adjacent': [68, 69, 81, 82, 100, 101, 117, 118], 'location': 'B', 'alleys': ['XQ', 'XR', 'WA']}, 
        100: {'adjacent': [83, 85, 99, 101, 102, 103, 118, 119], 'location': 'B', 'alleys': ['WB', 'WC', 'WI']}, 
        101: {'adjacent': [70, 82, 83, 84, 85, 99, 100, 103, 118], 'location': 'B', 'alleys': ['XR', 'XS', 'WB']}, 
        102: {'adjacent': [100, 103, 119], 'location': 'B', 'alleys': ['WC', 'WD']}, 
        103: {'adjacent': [83, 85, 100, 101, 102], 'location': 'B', 'alleys': ['WC', 'WD']}, 
        104: {'adjacent': [105, 121, 122, 123], 'location': 'B', 'alleys': ['WD', 'WJ']}, 
        105: {'adjacent': [86, 88, 89, 104, 106, 123], 'location': 'B', 'alleys': ['WD', 'WE', 'WK']}, 
        106: {'adjacent': [89, 105, 107, 126, 127], 'location': 'B', 'alleys': ['WK', 'WF']}, 
        107: {'adjacent': [89, 106, 108, 126, 127, 128], 'location': 'B', 'alleys': ['WF', 'WG', 'WL']}, 
        108: {'adjacent': [89, 93, 94, 107, 109, 110, 111, 112, 127, 128, 130], 'location': 'B', 'alleys': ['WG', 'XZ', 'WN']}, 
        109: {'adjacent': [91, 92, 93, 94, 108, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XZ', 'XY']}, 
        110: {'adjacent': [93, 94, 108, 109, 111, 112, 130], 'location': 'H3', 'alleys': [' ']}, 
        111: {'adjacent': [93, 94, 108, 109, 110, 112, 130], 'location': 'H4', 'alleys': [' ']}, 
        112: {'adjacent': [93, 94, 108, 109, 110, 111, 114, 130, 131, 132, 145, 147], 'location': 'B', 'alleys': [' ']}, 
        113: {'adjacent': [96, 97, 98, 114, 115, 116], 'location': 'H4', 'alleys': [' ']}, 
        114: {'adjacent': [96, 97, 98, 112, 113, 115, 116, 131, 132, 145, 147], 'location': 'B', 'alleys': ['WO']}, 
        115: {'adjacent': [96, 97, 98, 113, 114, 116, 133], 'location': 'B', 'alleys': ['WO', 'WH']}, 
        116: {'adjacent': [96, 97, 98, 113, 114, 115, 133], 'location': 'B', 'alleys': ['WH']}, 
        117: {'adjacent': [81, 99, 118, 134], 'location': 'W3', 'alleys': ['WI']}, 
        118: {'adjacent': [81, 99, 100, 101, 117], 'location': 'B', 'alleys': ['WA', 'WI']}, 
        119: {'adjacent': [100, 102, 121, 134], 'location': 'W3', 'alleys': ['WI', 'WD']}, 
        120: {'adjacent': [135, 139, 153, 155], 'location': 'W3', 'alleys': ['WP', 'WU']}, 
        121: {'adjacent': [104, 119, 122, 134], 'location': 'W3', 'alleys': ['WP', 'WD']}, 
        122: {'adjacent': [104, 121, 123, 124, 139, 140, 161, 162], 'location': 'W3', 'alleys': ['WP', 'WJ', 'WQ']}, 
        123: {'adjacent': [104, 105, 122, 124], 'location': 'W3', 'alleys': ['WJ', 'WK']}, 
        124: {'adjacent': [122, 123, 125], 'location': 'B', 'alleys': ['WK', 'WQ']}, 
        125: {'adjacent': [124, 126, 140, 141], 'location': 'B', 'alleys': ['WK', 'WQ']}, 
        126: {'adjacent': [106, 107, 125, 127, 128, 129, 140, 141], 'location': 'B', 'alleys': ['WK', 'WM', 'WR']}, 
        127: {'adjacent': [106, 107, 108, 126, 128], 'location': 'B', 'alleys': ['WM', 'WL']}, 
        128: {'adjacent': [107, 108, 126, 127, 129], 'location': 'B', 'alleys': ['WM', 'WN']}, 
        129: {'adjacent': [126, 128, 130, 142, 143], 'location': 'W4', 'alleys': ['WN', 'WR']}, 
        130: {'adjacent': [93, 94, 108, 109, 110, 111, 112, 129, 142, 143], 'location': 'W4', 'alleys': ['WN']}, 
        131: {'adjacent': [112, 114, 132, 145, 147], 'location': 'H3', 'alleys': [' ']}, 
        132: {'adjacent': [112, 114, 131, 133, 145, 147, 149], 'location': 'W4', 'alleys': ['WO', 'WS']}, 
        133: {'adjacent': [115, 116, 132, 149, 151], 'location': 'W4', 'alleys': ['WO', 'WT']}, 
        134: {'adjacent': [117, 119, 120, 121, 135, 153, 155], 'location': 'W3', 'alleys': ['WI', 'WP']}, 
        135: {'adjacent': [120, 134, 136, 137, 153, 155], 'location': 'W3', 'alleys': ['WU', 'WY']}, 
        136: {'adjacent': [135, 137, 156, 158], 'location': 'W3', 'alleys': ['WY']}, 
        137: {'adjacent': [135, 136, 138, 139], 'location': 'W3', 'alleys': ['WU']}, 
        138: {'adjacent': [137, 139], 'location': 'H2', 'alleys': [' ']}, 
        139: {'adjacent': [120, 122, 137, 138, 140, 160, 161, 162], 'location': 'W3', 'alleys': ['WU', 'WP']}, 
        140: {'adjacent': [122, 125, 126, 139, 141, 161, 162], 'location': 'B', 'alleys': ['WQ', 'WV']}, 
        141: {'adjacent': [125, 126, 140, 162, 164], 'location': 'B', 'alleys': ['WV', 'WR']}, 
        142: {'adjacent': [129, 130, 143, 165, 166], 'location': 'W4', 'alleys': ['WR']}, 
        143: {'adjacent': [129, 130, 142], 'location': 'H3', 'alleys': [' ']}, 
        144: {'adjacent': [145, 146, 168], 'location': 'H3', 'alleys': [' ']}, 
        145: {'adjacent': [112, 114, 131, 132, 144, 146, 147, 168], 'location': 'W4', 'alleys': ['WW']}, 
        146: {'adjacent': [144, 145, 148, 168, 169, 170], 'location': 'W4', 'alleys': ['WW', 'VA']}, 
        147: {'adjacent': [112, 114, 131, 132, 145, 148, 149, 150], 'location': 'W4', 'alleys': ['WS', 'WW']}, 
        148: {'adjacent': [146, 147, 149, 150, 169, 170], 'location': 'W4', 'alleys': ['WW', 'WX']}, 
        149: {'adjacent': [132, 133, 147, 148, 150], 'location': 'W4', 'alleys': ['WS', 'WT']}, 
        150: {'adjacent': [147, 148, 149, 151, 172], 'location': 'W4', 'alleys': ['WT', 'WX']}, 
        151: {'adjacent': [133, 150, 172], 'location': 'W4', 'alleys': ['WT']}, 
        152: {'adjacent': [153, 154], 'location': 'W3', 'alleys': [' ']}, 
        153: {'adjacent': [120, 134, 135, 152, 155], 'location': 'W3', 'alleys': [' ']}, 
        154: {'adjacent': [152, 155, 156, 157, 159, 174, 175], 'location': 'H1', 'alleys': [' ']}, 
        155: {'adjacent': [120, 134, 135, 153, 154, 156, 157, 159, 174, 175], 'location': 'W3', 'alleys': ['WY']}, 
        156: {'adjacent': [136, 154, 155, 157, 158, 159, 174, 175], 'location': 'W3', 'alleys': ['WY']}, 
        157: {'adjacent': [154, 155, 156, 159, 174, 175], 'location': 'H2', 'alleys': [' ']}, 
        158: {'adjacent': [136, 156], 'location': 'H2', 'alleys': [' ']}, 
        159: {'adjacent': [154, 155, 156, 157, 160, 174, 175, 177], 'location': 'W3', 'alleys': ['VC']}, 
        160: {'adjacent': [139, 159, 177], 'location': 'H2', 'alleys': [' ']}, 
        161: {'adjacent': [122, 139, 140, 162, 163, 176, 177, 178, 179], 'location': 'W3', 'alleys': ['VD', 'WZ']}, 
        162: {'adjacent': [122, 139, 140, 141, 161, 164], 'location': 'B', 'alleys': ['WV', 'WZ']}, 
        163: {'adjacent': [161, 164, 178, 180, 181], 'location': 'B', 'alleys': ['WZ', 'VE']}, 
        164: {'adjacent': [141, 162, 163, 180, 181], 'location': 'B', 'alleys': ['WZ', 'WR']}, 
        165: {'adjacent': [142, 166, 181, 183, 184], 'location': 'W4', 'alleys': ['WR']}, 
        166: {'adjacent': [142, 165], 'location': 'H3', 'alleys': [' ']}, 
        167: {'adjacent': [168, 186], 'location': 'H3', 'alleys': [' ']}, 
        168: {'adjacent': [144, 145, 146, 167, 186], 'location': 'W4', 'alleys': ['VA']}, 
        169: {'adjacent': [146, 148, 170, 171, 187, 188], 'location': 'W4', 'alleys': ['VA', 'VB']}, 
        170: {'adjacent': [146, 148, 169, 171, 172], 'location': 'W4', 'alleys': ['WX', 'VB']}, 
        171: {'adjacent': [169, 170, 172, 187, 188], 'location': 'W4', 'alleys': ['VB']}, 
        172: {'adjacent': [150, 151, 170, 171], 'location': 'W4', 'alleys': ['WX']}, 
        173: {'adjacent': [174, 175, 189], 'location': 'W3', 'alleys': ['VH']}, 
        174: {'adjacent': [154, 155, 156, 157, 159, 173, 175], 'location': 'H1', 'alleys': [' ']}, 
        175: {'adjacent': [154, 155, 156, 157, 159, 173, 174, 176, 177, 189], 'location': 'W3', 'alleys': ['VC', 'VH', 'VI']}, 
        176: {'adjacent': [161, 175, 178, 179, 189], 'location': 'W3', 'alleys': ['VI']}, 
        177: {'adjacent': [159, 160, 161, 175, 176, 178, 179], 'location': 'W3', 'alleys': ['VC', 'VI']}, 
        178: {'adjacent': [161, 163, 176, 177, 179], 'location': 'W3', 'alleys': ['VD', 'VE']}, 
        179: {'adjacent': [161, 176, 177, 178, 180, 182], 'location': 'B', 'alleys': ['VE']}, 
        180: {'adjacent': [163, 164, 179, 181, 182], 'location': 'B', 'alleys': ['VE', 'VF']}, 
        181: {'adjacent': [163, 164, 165, 180, 183, 184], 'location': 'B', 'alleys': ['WR', 'VF']}, 
        182: {'adjacent': [179, 180, 183, 185], 'location': 'B', 'alleys': ['VF']}, 
        183: {'adjacent': [165, 181, 182, 184, 185], 'location': 'W4', 'alleys': ['VF']}, 
        184: {'adjacent': [165, 181, 183], 'location': 'H3', 'alleys': [' ']}, 
        185: {'adjacent': [182, 183, 186, 187, 188], 'location': 'W4', 'alleys': [' ']}, 
        186: {'adjacent': [167, 168, 185, 187, 188], 'location': 'W4', 'alleys': ['VA']}, 
        187: {'adjacent': [169, 171, 185, 186, 188], 'location': 'W4', 'alleys': ['VA', 'VG']}, 
        188: {'adjacent': [169, 171, 185, 186, 187], 'location': 'W4', 'alleys': ['VG']}, 
        189: {'adjacent': [173, 175, 176], 'location': 'W3', 'alleys': ['VH']}}

    # INVESTIGATOR_DICT contains information relevant to the investigator's movements
    # keys correspond to the manually labeled squares investigators can occupy
    # 'adj squares': investigator squares adjacent to the key
    # 'adj circles': Jack's circles adjacent to the key
    # Note: keys of length 3 correspond to allowed starting locations for investigators
    INVESTIGATOR_DICT = {'HA': {'adj squares': ['HB', 'HR', 'HQ'], 'adj circles': [1, 8, 9]}, 
        'HB': {'adj squares': ['HA', 'HC', 'HS'], 'adj circles': [1, 9, 11]}, 
        'HC': {'adj squares': ['HB', 'HD', 'HT'], 'adj circles': [12]}, 
        'HD': {'adj squares': ['HE', 'HF', 'HU', 'HC'], 'adj circles': [2, 14]}, 
        'HE': {'adj squares': ['HD', 'HF', 'HG'], 'adj circles': [2]}, 
        'HF': {'adj squares': ['HD', 'HE', 'HG', 'HU'], 'adj circles': [2, 16]}, 
        'HG': {'adj squares': ['HE', 'HF', 'HU', 'HH', 'HV', 'HI'], 'adj circles': [16, 17, 3]}, 
        'HH': {'adj squares': ['HG', 'HI', 'HV', 'HW'], 'adj circles': [3, 18]}, 
        'HI': {'adj squares': ['HG', 'HH', 'HJ', 'HX', 'HY'], 'adj circles': [3, 4]}, 
        'HJ': {'adj squares': ['HI', 'HK', 'HY', 'HZ'], 'adj circles': [4, 5, 20]}, 
        'HK': {'adj squares': ['HJ', 'HL', 'HZ', 'AA'], 'adj circles': [5, 22, 23]}, 
        'HL': {'adj squares': ['HK', 'HM', 'AB', 'AA', 'AL', 'AK'], 'adj circles': [23, 6, 24]}, 
        'HM': {'adj squares': ['HL', 'HN', 'HO', 'AB'], 'adj circles': [6, 25]}, 
        'HN': {'adj squares': ['HM', 'HO', 'HP'], 'adj circles': [7, 25]}, 
        'HO': {'adj squares': ['HM', 'HN', 'HP', 'AB', 'AM'], 'adj circles': [25, 45]}, 
        'HP': {'adj squares': ['HN', 'HO', 'AC', 'AM'], 'adj circles': [7, 26, 27]}, 
        'HQ': {'adj squares': ['HA', 'HR', 'AN'], 'adj circles': [8, 28]}, 
        'HR': {'adj squares': ['HA', 'HQ', 'AD', 'HS'], 'adj circles': [10, 29]}, 
        'HS': {'adj squares': ['HR', 'HB', 'AE'], 'adj circles': [10, 11]}, 
        'HT': {'adj squares': ['HC', 'HD', 'HU', 'AF'], 'adj circles': [12, 13, 14]}, 
        'HU': {'adj squares': ['HT', 'AF', 'HD', 'AG', 'HF', 'HG'], 'adj circles': [13, 14, 15, 16]}, 
        'HV': {'adj squares': ['HG', 'HH', 'AG', 'AH'], 'adj circles': [17, 18]}, 
        'HW': {'adj squares': ['HH', 'HX', 'AH', 'AS', 'AT'], 'adj circles': [19, 37]}, 
        'HX': {'adj squares': ['HI', 'HW', 'HY', 'AT'], 'adj circles': [19, 38]}, 
        'HY': {'adj squares': ['HI', 'HX', 'HJ', 'HZ', 'AI'], 'adj circles': [20, 21]}, 
        'HZ': {'adj squares': ['HY', 'HJ', 'HK', 'AA', 'AI'], 'adj circles': [20, 21, 22]}, 
        'AA': {'adj squares': ['HZ', 'HK', 'HL', 'AJ', 'AI'], 'adj circles': [22, 23, 41]}, 
        'AB': {'adj squares': ['HM', 'HL', 'HO', 'AK', 'AL', 'AM'], 'adj circles': [24, 45]}, 
        'AC': {'adj squares': ['HP', 'AM', 'AY'], 'adj circles': [26, 27, 47]}, 
        'AD': {'adj squares': ['HR', 'AN', 'AE', 'AO'], 'adj circles': [29, 30, 31]}, 
        'AE': {'adj squares': ['HS', 'AD', 'HT', 'HU', 'AF', 'AP'], 'adj circles': [13, 32]}, 
        'AF': {'adj squares': ['HT', 'HU', 'AE', 'AG', 'AP', 'AQ'], 'adj circles': [13, 33]}, 
        'AG': {'adj squares': ['HU', 'HV', 'AF', 'AP', 'AQ', 'AH'], 'adj circles': [15, 33, 34]}, 
        'AH': {'adj squares': ['AV', 'HW', 'AG', 'AQ', 'AT', 'AS', 'AR'], 'adj circles': [34, 35, 37]}, 
        'AI': {'adj squares': ['HY', 'HZ', 'AA', 'AT'], 'adj circles': [21, 41]}, 
        'AJ': {'adj squares': ['AA', 'AK', 'AU', 'AV'], 'adj circles': [42]}, 
        'AK': {'adj squares': ['AJ', 'HL', 'AB', 'AL'], 'adj circles': [24, 44]}, 
        'AL': {'adj squares': ['HL', 'AK', 'AB', 'AM', 'AW', 'AX', 'BI'], 'adj circles': [24, 46]}, 
        'AM': {'adj squares': ['AB', 'HO', 'HP', 'AC', 'AX', 'BI'], 'adj circles': [45, 46, 26]}, 
        'AN': {'adj squares': ['HQ', 'AD', 'AZ', 'BA'], 'adj circles': [28, 48, 30]}, 
        'AO': {'adj squares': ['AD', 'BA', 'BL', 'BB', 'AP'], 'adj circles': [31, 51]}, 
        'AP': {'adj squares': ['AO', 'AE', 'AF', 'AG', 'AQ', 'BB', 'BC'], 'adj circles': [32, 33, 53]}, 
        'AQ': {'adj squares': ['AP', 'AF', 'AG', 'AR', 'AH', 'BC'], 'adj circles': [33, 34, 54]}, 
        'AR': {'adj squares': ['AQ', 'BD', 'AH', 'AS'], 'adj circles': [35, 54]}, 
        'AS': {'adj squares': ['AH', 'AR', 'BD', 'BM', 'HW', 'AT', 'BE'], 'adj circles': [36, 37, 56]}, 
        'AT': {'adj squares': ['HW', 'AH', 'AS', 'HX', 'AI', 'AU', 'BE', 'BF'], 'adj circles': [37, 38, 39, 40]}, 
        'AU': {'adj squares': ['AT', 'BF', 'BG', 'AV', 'AJ'], 'adj circles': [40, 42, 59]}, 
        'AV': {'adj squares': ['AU', 'AJ', 'AK', 'BG', 'AW', 'BH'], 'adj circles': [42, 43, 44, 59]}, 
        'AW': {'adj squares': ['AV', 'AL', 'BG', 'BH', 'AV'], 'adj circles': [43, 44]}, 
        'AX': {'adj squares': ['AL', 'AM', 'BH', 'BX', 'BI'], 'adj circles': [46, 62, 63]}, 
        'AY': {'adj squares': ['AC', 'BI', 'BJ'], 'adj circles': [47, 65, 67]}, 
        'AZ': {'adj squares': ['AN', 'BA', 'BK'], 'adj circles': [48, 49]}, 
        'BA': {'adj squares': ['AZ', 'AN', 'AO', 'BK', 'BO', 'BL', 'BB'], 'adj circles': [49, 50, 51]}, 
        'BB': {'adj squares': ['BA', 'AO', 'AP', 'BC', 'BL', 'BP', 'BQ'], 'adj circles': [51, 52, 53]}, 
        'BC': {'adj squares': ['BB', 'AP', 'BD', 'AQ', 'BQ', 'BR'], 'adj circles': [53, 54, 55]}, 
        'BD': {'adj squares': ['AR', 'BC', 'AS', 'BS'], 'adj circles': [36]}, 
        'BE': {'adj squares': ['AS', 'AT', 'BF', 'BM', 'BT'], 'adj circles': [39, 56, 57]}, 
        'BF': {'adj squares': ['BE', 'AU', 'BU', 'BG'], 'adj circles': [58]}, 
        'BG': {'adj squares': ['BU', 'BF', 'AU', 'AV', 'AW', 'BH', 'BV'], 'adj circles': [58, 59, 43]}, 
        'BH': {'adj squares': ['BG', 'AV', 'AW', 'AX', 'BX', 'BV', 'BW'], 'adj circles': [43, 60, 61, 62]}, 
        'BI': {'adj squares': ['AX', 'AL', 'AM', 'AY', 'BY'], 'adj circles': [46, 65]}, 
        'BJ': {'adj squares': ['AY', 'BY'], 'adj circles': [64, 66, 67]}, 
        'BK': {'adj squares': ['AZ', 'BA', 'BN', 'BO'], 'adj circles': [50]}, 
        'BL': {'adj squares': ['BO', 'BA', 'AO', 'BB', 'BP'], 'adj circles': [51]}, 
        'BM': {'adj squares': ['AS', 'BE', 'BS', 'BT'], 'adj circles': [56, 73]}, 
        'BN': {'adj squares': ['BK', 'BO', 'CA'], 'adj circles': [68]}, 
        'BO': {'adj squares': ['CA', 'BN', 'BK', 'BA', 'BL', 'BP'], 'adj circles': [50, 68, 69]}, 
        'BP': {'adj squares': ['CA', 'BO', 'BL', 'BB', 'BQ', 'CI'], 'adj circles': [52, 69, 70]}, 
        'BQ': {'adj squares': ['BP', 'BB', 'BC', 'BR', 'CB'], 'adj circles': [52, 55, 71]}, 
        'BR': {'adj squares': ['CB', 'BQ', 'BC', 'BS', 'CC'], 'adj circles': [55, 71, 72]}, 
        'BS': {'adj squares': ['CC', 'BR', 'BD', 'BM', 'BT'], 'adj circles': [72, 73]}, 
        'BT': {'adj squares': ['BS', 'BM', 'BE', 'BU', 'CD'], 'adj circles': [57, 73, 74]}, 
        'BU': {'adj squares': ['BT', 'BF', 'BG', 'BV', 'CD', 'CL', 'CE'], 'adj circles': [58, 75, 76]}, 
        'BV': {'adj squares': ['CE', 'BU', 'BG', 'BH', 'BW', 'CM'], 'adj circles': [60, 76]},
        'BW': {'adj squares': ['CM', 'BBB', 'BV'], 'adj circles': [77, 78]},  
        'BX': {'adj squares': ['BH', 'AX'], 'adj circles': [61, 63]}, 
        'BY': {'adj squares': ['BI', 'BJ', 'BZ', 'CO'], 'adj circles': [64, 97]}, 
        'BZ': {'adj squares': ['BY', 'CF'], 'adj circles': [79, 80]}, 
        'CA': {'adj squares': ['BN', 'BO', 'BP', 'CG'], 'adj circles': [68, 69, 81]}, 
        'CB': {'adj squares': ['BQ', 'BR', 'CJ', 'CI'], 'adj circles': [71, 84]}, 
        'CC': {'adj squares': ['BR', 'BS', 'CJ', 'AAA'], 'adj circles': [72, 87]}, 
        'CD': {'adj squares': ['AAA', 'BT', 'CK', 'CL'], 'adj circles': [74, 75]}, 
        'CE': {'adj squares': ['CL', 'BU', 'BV', 'BBB'], 'adj circles': [76]}, 
        'CF': {'adj squares': ['BZ', 'CN'], 'adj circles': [79, 94, 95]}, 
        'CG': {'adj squares': ['CA', 'CH', 'CP', 'CQ'], 'adj circles': [82, 99]}, 
        'CH': {'adj squares': ['CG', 'CI', 'CQ', 'CR'], 'adj circles': [82, 101]}, 
        'CI': {'adj squares': ['CH', 'BP', 'CB', 'CS'], 'adj circles': [70, 83, 84]}, 
        'CJ': {'adj squares': ['CS', 'CB', 'CC', 'AAA', 'CCC'], 'adj circles': [85, 86, 87]}, 
        'CK': {'adj squares': ['CD', 'CL', 'CT', 'CU', 'CCC'], 'adj circles': [89, 90, 91]}, 
        'CL': {'adj squares': ['CD', 'CE', 'CK', 'DDD', 'BU'], 'adj circles': [75, 90, 92]}, 
        'CM': {'adj squares': ['BW', 'BBB'], 'adj circles': [77, 78]}, 
        'CN': {'adj squares': ['CF', 'CV'], 'adj circles': [94, 111]}, 
        'CO': {'adj squares': ['BY', 'CW', 'DD'], 'adj circles': [97, 98, 116]}, 
        'CP': {'adj squares': ['CA', 'CG', 'CQ', 'CX'], 'adj circles': [81, 99]}, 
        'CQ': {'adj squares': ['CG', 'CP', 'CH', 'CR', 'CY'], 'adj circles': [99, 101]}, 
        'CR': {'adj squares': ['CH', 'CQ', 'CY', 'CS', 'DE'], 'adj circles': [100, 101]}, 
        'CS': {'adj squares': ['CR', 'CI', 'CJ', 'CZ'], 'adj circles': [83, 85, 103]}, 
        'CT': {'adj squares': ['CK', 'CU', 'CCC', 'EEE', 'FFF'], 'adj circles': [89, 105, 106]}, 
        'CU': {'adj squares': ['CK', 'CT', 'DB', 'DA', 'CCC', 'FFF', 'DH'], 'adj circles': [89, 107, 108]}, 
        'CV': {'adj squares': ['CN', 'DB', 'DI', 'BBB', 'DDD'], 'adj circles': [93, 109, 112]}, 
        'CW': {'adj squares': ['CO', 'DC'], 'adj circles': [96]}, 
        'CX': {'adj squares': ['CP', 'CY', 'DJ'], 'adj circles': [117, 118]}, 
        'CY': {'adj squares': ['CX', 'CQ', 'CR', 'DE'], 'adj circles': [118, 100]}, 
        'CZ': {'adj squares': ['CS', 'DE'], 'adj circles': [102, 103]}, 
        'DA': {'adj squares': ['DH', 'DB', 'CU', 'DO'], 'adj circles': [108, 128]}, 
        'DB': {'adj squares': ['DA', 'CU', 'CV', 'DP'], 'adj circles': [108, 110, 130]}, 
        'DC': {'adj squares': ['CW', 'DD', 'DI'], 'adj circles': [113, 114, 115]}, 
        'DD': {'adj squares': ['CO', 'DC', 'DS', 'DR'], 'adj circles': [115, 116, 133]}, 
        'DE': {'adj squares': ['CY', 'CR', 'CZ', 'DK'], 'adj circles': [100, 102, 119]}, 
        'DF': {'adj squares': ['DM', 'DK', 'DV', 'EEE'], 'adj circles': [104, 121, 122]}, 
        'DG': {'adj squares': ['DH', 'DO', 'EE', 'FFF'], 'adj circles': [126, 127]}, 
        'DH': {'adj squares': ['DG', 'DA', 'CU', 'FFF'], 'adj circles': [107, 127]}, 
        'DI': {'adj squares': ['CV', 'DC', 'DR', 'DQ'], 'adj circles': [114, 112, 132]}, 
        'DJ': {'adj squares': ['CX', 'DK', 'EA'], 'adj circles': [117, 134]}, 
        'DK': {'adj squares': ['DJ', 'EA', 'DE', 'DF'], 'adj circles': [119, 121, 134]}, 
        'DL': {'adj squares': ['DT', 'DV', 'DU'], 'adj circles': [120, 139]}, 
        'DM': {'adj squares': ['DF', 'DV', 'DN', 'EEE'], 'adj circles': [122, 123, 124]}, 
        'DN': {'adj squares': ['DM', 'ED'], 'adj circles': [124, 125]}, 
        'DO': {'adj squares': ['DA', 'DG', 'DP', 'EE'], 'adj circles': [126, 128, 129]}, 
        'DP': {'adj squares': ['DO', 'DW', 'DB'], 'adj circles': [129, 130]}, 
        'DQ': {'adj squares': ['DI', 'DX'], 'adj circles': [131]}, 
        'DR': {'adj squares': ['DI', 'DD', 'DS', 'DY'], 'adj circles': [132, 133, 149]}, 
        'DS': {'adj squares': ['DD', 'DR', 'DZ'], 'adj circles': [133, 151]}, 
        'DT': {'adj squares': ['EA', 'DL'], 'adj circles': [120]}, 
        'DU': {'adj squares': ['EB', 'DL', 'DV', 'EL'], 'adj circles': [137, 138, 139]}, 
        'DV': {'adj squares': ['DU', 'DL', 'EL', 'DF', 'DM', 'EC'], 'adj circles': [139, 122]}, 
        'DW': {'adj squares': ['DP', 'EF'], 'adj circles': [142, 143]}, 
        'DX': {'adj squares': ['DQ', 'DY', 'EG'], 'adj circles': [145, 147]}, 
        'DY': {'adj squares': ['DX', 'DR', 'DZ', 'EH'], 'adj circles': [147, 148, 149, 150]}, 
        'DZ': {'adj squares': ['DY', 'DS', 'EP'], 'adj circles': [150, 151, 172]}, 
        'EA': {'adj squares': ['DJ', 'DK', 'DT', 'EB', 'EI', 'EJ'], 'adj circles': [134, 135, 153, 155]}, 
        'EB': {'adj squares': ['EA', 'EK', 'DU'], 'adj circles': [135, 136, 137]}, 
        'EC': {'adj squares': ['DV', 'ED', 'EM'], 'adj circles': [140]}, 
        'ED': {'adj squares': ['EC', 'DN', 'EE'], 'adj circles': [140, 125]}, 
        'EE': {'adj squares': ['ED', 'DG', 'DO', 'EN'], 'adj circles': [126, 141]}, 
        'EF': {'adj squares': ['DW', 'EX'], 'adj circles': [142, 165, 166]}, 
        'EG': {'adj squares': ['DX', 'EH', 'EY'], 'adj circles': [144, 145, 146, 168]}, 
        'EH': {'adj squares': ['EG', 'DY', 'EO'], 'adj circles': [146, 148]}, 
        'EI': {'adj squares': ['EA', 'EQ'], 'adj circles': [152, 153]}, 
        'EJ': {'adj squares': ['EA', 'EQ', 'EK', 'ER'], 'adj circles': [154, 155, 156]}, 
        'EK': {'adj squares': ['EJ', 'EB'], 'adj circles': [156, 158, 136]}, 
        'EL': {'adj squares': ['DL', 'DU', 'DV', 'EU'], 'adj circles': [160, 139]}, 
        'EM': {'adj squares': ['EC', 'EN', 'EV', 'FG'], 'adj circles': [161, 162]}, 
        'EN': {'adj squares': ['EM', 'EE', 'EW'], 'adj circles': [141, 162, 164]}, 
        'EO': {'adj squares': ['EH', 'EP', 'EZ'], 'adj circles': [169, 170]}, 
        'EP': {'adj squares': ['DZ', 'EO', 'FA'], 'adj circles': [170, 171, 172]}, 
        'EQ': {'adj squares': ['EI', 'EJ'], 'adj circles': [152, 154]}, 
        'ER': {'adj squares': ['EJ', 'ES', 'FB', 'FC', 'FD', 'FF'], 'adj circles': [174, 175]}, 
        'ES': {'adj squares': ['ER', 'ET', 'FC', 'FD', 'FF'], 'adj circles': [157, 159, 175]}, 
        'ET': {'adj squares': ['ES', 'EU', 'FD', 'FG'], 'adj circles': [159, 177]}, 
        'EU': {'adj squares': ['EL', 'ET', 'FD', 'FG'], 'adj circles': [160, 177]}, 
        'EV': {'adj squares': ['EM', 'FG', 'FH', 'EW'], 'adj circles': [161, 163, 178]}, 
        'EW': {'adj squares': ['EV', 'EN', 'FI', 'EX'], 'adj circles': [163, 164, 180, 181]}, 
        'EX': {'adj squares': ['EW', 'EF', 'FJ'], 'adj circles': [165, 181, 183, 184]}, 
        'EY': {'adj squares': ['EG', 'FK'], 'adj circles': [167, 168, 186]}, 
        'EZ': {'adj squares': ['EO', 'FA', 'FL'], 'adj circles': [169, 187]}, 
        'FA': {'adj squares': ['EP', 'EZ', 'FL'], 'adj circles': [171, 188]}, 
        'FB': {'adj squares': ['ER', 'FC', 'FE'], 'adj circles': [173, 174]}, 
        'FC': {'adj squares': ['FB', 'FE', 'ER', 'ES', 'FD', 'FF'], 'adj circles': [173, 175]}, 
        'FD': {'adj squares': ['ER', 'ES', 'ET', 'FC', 'FF', 'FG'], 'adj circles': [175, 177]}, 
        'FE': {'adj squares': ['FB', 'FC', 'FF'], 'adj circles': [173, 189]}, 
        'FF': {'adj squares': ['FE', 'FC', 'ER', 'ES', 'FD', 'FG'], 'adj circles': [189, 175, 176]}, 
        'FG': {'adj squares': ['FF', 'FD', 'ET', 'EU', 'EM', 'EV', 'FH'], 'adj circles': [176, 177, 161]}, 
        'FH': {'adj squares': ['FG', 'EV', 'FI'], 'adj circles': [178, 179]}, 
        'FI': {'adj squares': ['FH', 'EW', 'FJ'], 'adj circles': [179, 180, 182]}, 
        'FJ': {'adj squares': ['FI', 'EX', 'FK'], 'adj circles': [182, 183, 185]}, 
        'FK': {'adj squares': ['FJ', 'EY', 'FL'], 'adj circles': [185, 186]}, 
        'FL': {'adj squares': ['FK', 'EZ', 'FA'], 'adj circles': [187, 188]},
        'AAA': {'adj squares': ['CJ', 'CC', 'CD', 'CCC'], 'adj circles': [87, 88]},
        'BBB': {'adj squares': ['CL', 'CE', 'CM', 'CV', 'DDD', 'BW'], 'adj circles': [92, 93, 77]}, 
        'CCC': {'adj squares': ['AAA', 'CJ', 'EEE', 'CT', 'CK', 'CU'], 'adj circles': [86, 88, 89, 105]}, 
        'DDD': {'adj squares': ['BBB', 'CL', 'CV', 'CK'], 'adj circles': [91, 92, 109]}, 
        'EEE': {'adj squares': ['CCC', 'CT', 'DF', 'DM'], 'adj circles': [104, 105, 123]}, 
        'FFF': {'adj squares': ['CT', 'CU', 'DG', 'DH'], 'adj circles':[106, 107]}}

    # Dictionaries for each of the four white circle quadrants
    W1, W2, W3, W4 = quads(JACK_DICT)

    SPECIAL_MOVEMENTS = {'coach':{'int':1, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0},
     'alley':{'int':2, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0}, 
     'boat':{'int':3, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0}}

    # begin the game
    print("Welcome to Whitehall Mystery!")
    print("Get ready to go head to head with Jack the AI!")
    DISCOVERY_LOCATIONS = pick_DL(W1, W2, W3, W4)        # Jack picks Discovery Locations
    print("Jack has picked his Discovery Locations")
    jack_loc = pick_loc(DISCOVERY_LOCATIONS)                        # Jack picks starting location from Discovery Locations
    COPY_OF_DISCOVERY_LOCATIONS = DISCOVERY_LOCATIONS
    COPY_OF_DISCOVERY_LOCATIONS.remove(jack_loc)
    goal_loc = pick_loc(COPY_OF_DISCOVERY_LOCATIONS)
    INVESTIGATOR_LOCATIONS = input_investigator_loc()                                   # The Investigators input their starting locations
    print(f"Jack: I'm at my starting location, {jack_loc}. Come and get me!")

    round = 0             # iterator to keep track of the round (out of 4 rounds)
    turn = 0              # iterator to keep track of the turn (15 turns for each round)
    jack_win = 1          # boolean to keep track if Jack is winning
    CLUES = []
    JACK_LOCATIONS = []
    while round < 5:
        round, turn, CLUES, JACK_LOCATIONS = next_round(round, turn, CLUES, JACK_LOCATIONS)
        JACK_LOCATIONS.append(jack_loc)
        print(f"Round {round}")
        while turn <= 15:
            turn += 1
            # Jack: Escape the Night
            # TODO: add functionality for special movements, if desired
            jack_loc = jack_move(jack_loc, JACK_DICT, goal_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT) # TODO: add inputs for AI for movement
            JACK_LOCATIONS.append(jack_loc)
            print("Jack has moved")
            at_goal = check_DL(jack_loc, COPY_OF_DISCOVERY_LOCATIONS)
            if at_goal:
                print("Jack has reached a Discovery Location.")
                COPY_OF_DISCOVERY_LOCATIONS.remove(jack_loc)
                print(f"Jack:'I'm at {jack_loc}, come and get me!")
                break  
            else:
                # Investigators: Hunting the Monster
                # Yellow move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[0], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                # Blue move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[1], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                # Red move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[2], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)

                # Investigators: Clues and Suspicion
                # Yellow investigate
                print("Jasper T.C. Waring (yellow):")
                yellow_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if yellow_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[0], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif yellow_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[0], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
                # Blue investigate
                print("Arthur Ferris (blue):")
                blue_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if blue_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[1], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif blue_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[1], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
                # Red investigate
                print("Thomas Bond (red):")
                red_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if red_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[2], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif red_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[2], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
        if jack_win == 0:
            print("Congratulations, investigators, you have won!")
            return jack_win
    print("Jack: Ha ha ha! I have won! Better luck next time, investigators!")
    return jack_win

def runAdminGame():
    """Runs a game of Whitehall Mystery
       Jack moves through AI
       Investigators move through players
       Relevant information is printed for maintenance
    """

    # Gameboard/rules data

    # JACK_DICT contains information relevant to Jack's movements
    # keys correspond to the numbered circles that Jack can occupy
    # 'adjacent': numbered circles adjacent to the key
    # 'location': which part of the board the key is in (white quadrants, black center, or water location)
    # 'alleys': which alleyways the key is adjacent to
    JACK_DICT = {1: {'adjacent': [2, 8, 9, 10, 11, 12, 14, 28, 29], 'location': 'W1', 'alleys': ['ZA']}, 
        2: {'adjacent': [1, 3, 9, 11, 12, 14, 16, 17], 'location': 'W1', 'alleys': ['ZF']}, 
        3: {'adjacent': [2, 4, 16, 17, 18, 19, 20, 21, 37, 38], 'location': 'W1', 'alleys': ['ZG', 'ZH']}, 
        4: {'adjacent': [3, 5, 19, 20, 21, 38], 'location': 'B', 'alleys': ['ZI']}, 
        5: {'adjacent': [4, 20, 22, 23], 'location': 'W2', 'alleys': ['ZJ']}, 
        6: {'adjacent': [23, 24, 25, 45], 'location': 'W2', 'alleys': ['ZM']}, 
        7: {'adjacent': [25, 26, 27, 45], 'location': 'W2', 'alleys': ['ZO']}, 
        8: {'adjacent': [1, 9, 10, 28, 29], 'location': 'W1', 'alleys': [' ']}, 
        9: {'adjacent': [1, 2, 8, 10, 11, 12, 14, 28, 29], 'location': 'W1', 'alleys': ['ZA', 'ZB']}, 
        10: {'adjacent': [1, 8, 9, 11, 13, 28, 29, 30, 31, 32], 'location': 'W1', 'alleys': ['ZB', 'ZS']}, 
        11: {'adjacent': [1, 2, 9, 10, 12, 13, 14, 29, 30, 31, 32], 'location': 'W1', 'alleys': ['ZB', 'ZC']}, 
        12: {'adjacent': [1, 2, 9, 11, 13, 14], 'location': 'W1', 'alleys': ['ZC', 'ZD']}, 
        13: {'adjacent': [10, 11, 12, 14, 15, 16, 29, 30, 31, 32, 33], 'location': 'W1', 'alleys': ['ZC', 'ZE', 'ZT', 'ZU']}, 
        14: {'adjacent': [1, 2, 9, 11, 12, 13, 15, 16], 'location': 'W1', 'alleys': ['ZD', 'ZE', 'ZF']}, 
        15: {'adjacent': [13, 14, 16, 17, 18, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZU', 'ZV']}, 
        16: {'adjacent': [2, 3, 13, 14, 15, 17], 'location': 'W1', 'alleys': ['ZF', 'ZV']}, 
        17: {'adjacent': [2, 3, 15, 16, 18, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZV', 'ZG']}, 
        18: {'adjacent': [3, 15, 17, 19, 33, 34, 35, 37], 'location': 'W1', 'alleys': ['ZG', 'ZW']}, 
        19: {'adjacent': [3, 4, 18, 20, 21, 37, 38], 'location': 'B', 'alleys': ['ZH', 'ZX']}, 
        20: {'adjacent': [3, 4, 5, 19, 21, 22, 38], 'location': 'B', 'alleys': ['ZI', 'ZJ', 'ZZ']}, 
        21: {'adjacent': [3, 4, 19, 20, 22, 36, 37, 38, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZZ', 'ZY', 'YA']}, 
        22: {'adjacent': [5, 20, 21, 23, 24, 41, 42, 44], 'location': 'B', 'alleys': ['ZJ', 'ZK', 'YA']}, 
        23: {'adjacent': [5, 6, 22, 24, 41, 42, 44], 'location': 'W2', 'alleys': ['ZK', 'ZL']}, 
        24: {'adjacent': [6, 22, 23, 25, 41, 42, 43, 44, 45, 46], 'location': 'W2', 'alleys': ['ZL', 'ZM', 'YD', 'VJ']}, 
        25: {'adjacent': [6, 7, 24, 26, 27, 45], 'location': 'W2', 'alleys': ['ZN', 'ZO']}, 
        26: {'adjacent': [7, 25, 27, 45, 46, 47], 'location': 'W2', 'alleys': ['ZP', 'ZQ', 'YE']}, 
        27: {'adjacent': [7, 25, 26, 45, 47], 'location': 'W2', 'alleys': ['ZQ']}, 
        28: {'adjacent': [1, 8, 9, 10, 29, 30, 48, 49, 50, 51], 'location': 'W1', 'alleys': ['ZR']}, 
        29: {'adjacent': [1, 8, 9, 10, 11, 13, 28, 30, 31, 32], 'location': 'W1', 'alleys': ['ZR', 'ZS']}, 
        30: {'adjacent': [10, 11, 13, 28, 29, 31, 32, 48, 49, 50, 51], 'location': 'W1', 'alleys': ['ZR', 'YH']}, 
        31: {'adjacent': [10, 11, 13, 29, 30, 32, 33, 51, 52, 53], 'location': 'W1', 'alleys': ['YH', 'YI']}, 
        32: {'adjacent': [10, 11, 13, 29, 30, 31, 33, 51, 52, 53], 'location': 'W1', 'alleys': ['YI', 'ZT']}, 
        33: {'adjacent': [13, 15, 17, 18, 31, 32, 34, 35, 37, 51, 52, 53, 54], 'location': 'W1', 'alleys': ['ZT', 'ZU', 'YJ', 'YK']}, 
        34: {'adjacent': [15, 17, 18, 33, 35, 37, 54], 'location': 'W1', 'alleys': ['YK', 'YL']}, 
        35: {'adjacent': [15, 17, 18, 34, 36, 37, 53, 54, 55, 72, 73], 'location': 'W1', 'alleys': ['YL', 'YM']}, 
        36: {'adjacent': [21, 37, 38, 39, 40, 41, 53, 54, 55, 56, 72, 73], 'location': 'W1', 'alleys': ['YM', 'YY']}, 
        37: {'adjacent': [3, 15, 17, 18, 19, 21, 33, 34, 35, 36, 38, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZW', 'ZX', 'YM']}, 
        38: {'adjacent': [3, 4, 19, 20, 21, 36, 37, 39, 40, 41, 56], 'location': 'B', 'alleys': ['ZX', 'ZY']}, 
        39: {'adjacent': [21, 36, 37, 38, 40, 41, 42, 56, 57, 58, 59], 'location': 'B', 'alleys': ['YN', 'YO']}, 
        40: {'adjacent': [21, 36, 37, 38, 39, 41, 42, 56, 57, 58, 59], 'location': 'B', 'alleys': ['YB', 'YO']}, 
        41: {'adjacent': [21, 22, 23, 24, 36, 37, 38, 39, 40, 42, 44, 56], 'location': 'B', 'alleys': ['YA', 'YB']}, 
        42: {'adjacent': [22, 23, 24, 39, 40, 41, 43, 44, 56, 57, 58, 59], 'location': 'W2', 'alleys': ['YB', 'ZL', 'YC', 'YP']}, 
        43: {'adjacent': [24, 42, 44, 46, 58, 59, 60, 61, 62, 76, 77, 78], 'location': 'W2', 'alleys': ['YQ', 'YR', 'YS', 'XD']}, 
        44: {'adjacent': [22, 23, 24, 41, 42, 43, 46, 59], 'location': 'W2', 'alleys': ['YC', 'YR', 'VJ']}, 
        45: {'adjacent': [6, 7, 24, 25, 26, 27, 46], 'location': 'W2', 'alleys': ['ZN', 'ZP', 'YD']}, 
        46: {'adjacent': [24, 26, 43, 44, 45, 62, 63, 64, 65, 79, 80, 97], 'location': 'W2', 'alleys': ['YD', 'YS', 'YE', 'XF']}, 
        47: {'adjacent': [26, 27, 65, 67], 'location': 'W2', 'alleys': ['YE']}, 
        48: {'adjacent': [28, 30, 49, 50, 51, 68], 'location': 'W1', 'alleys': ['YG']}, 
        49: {'adjacent': [28, 30, 48, 50, 51, 68], 'location': 'W1', 'alleys': ['YG', 'YT']}, 
        50: {'adjacent': [28, 30, 48, 49, 51, 52, 68, 69, 70], 'location': 'W1', 'alleys': ['YT', 'XG', 'TU']}, 
        51: {'adjacent': [28, 30, 31, 32, 33, 48, 49, 50, 52, 53, 68, 69, 70], 'location': 'W1', 'alleys': ['YH', 'YU', 'YV']}, 
        52: {'adjacent': [31, 32, 33, 50, 51, 53, 55, 68, 69, 70, 71], 'location': 'W1', 'alleys': ['YV', 'YW', 'XJ']}, 
        53: {'adjacent': [31, 32, 33, 35, 36, 51, 52, 54, 55, 72, 73], 'location': 'W1', 'alleys': ['YJ', 'YW']}, 
        54: {'adjacent': [33, 34, 35, 36, 53, 55, 72, 73], 'location': 'W1', 'alleys': ['YJ', 'YL']}, 
        55: {'adjacent': [35, 36, 52, 53, 54, 71, 72, 73, 87], 'location': 'W1', 'alleys': ['YW', 'YX', 'XK']}, 
        56: {'adjacent': [21, 36, 37, 38, 39, 40, 41, 42, 57, 58, 59, 73], 'location': 'B', 'alleys': ['YY', 'YN']}, 
        57: {'adjacent': [39, 40, 42, 56, 58, 59, 73, 74, 75, 76], 'location': 'B', 'alleys': ['YZ', 'XA']}, 
        58: {'adjacent': [39, 40, 42, 43, 56, 57, 59, 60, 73, 74, 75, 76, 77, 78], 'location': 'B', 'alleys': ['XA', 'XB', 'XC']}, 
        59: {'adjacent': [39, 40, 42, 43, 44, 56, 57, 58, 60, 76, 77, 78], 'location': 'B', 'alleys': ['XB', 'YP', 'YQ']}, 
        60: {'adjacent': [43, 58, 59, 61, 62, 76, 77, 78], 'location': 'W2', 'alleys': ['XD', 'XF']}, 
        61: {'adjacent': [43, 60, 62, 63], 'location': 'W2', 'alleys': ['XE', 'XF']}, 
        62: {'adjacent': [43, 46, 60, 61, 63], 'location': 'W2', 'alleys': ['YS', 'XE']}, 
        63: {'adjacent': [46, 61, 62], 'location': 'W2', 'alleys': ['XE', 'XF']}, 
        64: {'adjacent': [46, 65, 66, 67, 79, 80, 97], 'location': 'W2', 'alleys': ['YF']}, 
        65: {'adjacent': [46, 47, 64, 67, 79, 80, 97], 'location': 'W2', 'alleys': ['YE', 'YF']}, 
        66: {'adjacent': [64, 67], 'location': 'H5', 'alleys': [' ']}, 
        67: {'adjacent': [47, 64, 65, 66], 'location': 'W2', 'alleys': ['YF']}, 
        68: {'adjacent': [48, 49, 50, 51, 52, 69, 70, 81, 82, 99], 'location': 'W1', 'alleys': ['XG', 'XH']}, 
        69: {'adjacent': [50, 51, 52, 68, 70, 81, 82, 99], 'location': 'W1', 'alleys': ['XH', 'XI']}, 
        70: {'adjacent': [50, 51, 52, 68, 69, 82, 83, 84, 101], 'location': 'B', 'alleys': ['XI', 'XJ']}, 
        71: {'adjacent': [52, 55, 72, 84, 85, 86, 87], 'location': 'W1', 'alleys': ['XJ', 'XK', 'XL']}, 
        72: {'adjacent': [35, 36, 53, 54, 55, 71, 73, 87], 'location': 'W1', 'alleys': ['YX', 'XM']}, 
        73: {'adjacent': [35, 36, 53, 54, 55, 56, 57, 58, 72, 74, 75, 76], 'location': 'B', 'alleys': ['YY', 'YZ', 'XM']}, 
        74: {'adjacent': [57, 58, 73, 75, 76, 87, 88, 89, 90], 'location': 'B', 'alleys': ['XM', 'XN']}, 
        75: {'adjacent': [57, 58, 73, 74, 76, 77, 87, 88, 89, 90, 92, 93], 'location': 'B', 'alleys': ['XN', 'XO', 'XW']}, 
        76: {'adjacent': [43, 57, 58, 59, 60, 73, 74, 75, 77, 78, 90, 92, 93], 'location': 'B', 'alleys': ['XO', 'XC', 'VK']}, 
        77: {'adjacent': [43, 58, 59, 60, 75, 76, 78, 90, 92, 93], 'location': 'W2', 'alleys': ['VK', 'XP', 'XF']}, 
        78: {'adjacent': [43, 58, 59, 60, 76, 77], 'location': 'W2', 'alleys': ['XP', 'XF']}, 
        79: {'adjacent': [46, 64, 65, 80, 94, 95, 97], 'location': 'W2', 'alleys': ['XF']}, 
        80: {'adjacent': [46, 64, 65, 79, 97], 'location': 'H4', 'alleys': [' ']}, 
        81: {'adjacent': [68, 69, 82, 99, 117, 118], 'location': 'B', 'alleys': ['XQ']}, 
        82: {'adjacent': [68, 69, 70, 81, 83, 84, 99, 101], 'location': 'B', 'alleys': ['XI', 'XR']}, 
        83: {'adjacent': [70, 82, 84, 85, 100, 101, 103], 'location': 'B', 'alleys': ['XS', 'XT']}, 
        84: {'adjacent': [70, 71, 82, 83, 85, 86, 87, 101], 'location': 'B', 'alleys': ['XJ', 'XT']}, 
        85: {'adjacent': [71, 83, 84, 86, 87, 100, 101, 103], 'location': 'B', 'alleys': ['XT', 'WD']}, 
        86: {'adjacent': [71, 84, 85, 87, 88, 89, 105], 'location': 'B', 'alleys': ['XU', 'WD']}, 
        87: {'adjacent': [55, 71, 72, 74, 75, 84, 85, 86, 88, 89, 90], 'location': 'B', 'alleys': ['XU', 'XL', 'XM']}, 
        88: {'adjacent': [74, 75, 86, 87, 89, 90, 105], 'location': 'B', 'alleys': ['XU', 'XV']}, 
        89: {'adjacent': [74, 75, 86, 87, 88, 90, 91, 105, 106, 107, 108], 'location': 'B', 'alleys': ['XV', 'WE', 'XZ', 'WF']}, 
        90: {'adjacent': [74, 75, 76, 77, 87, 88, 89, 91, 92, 93], 'location': 'B', 'alleys': ['XW', 'XX']}, 
        91: {'adjacent': [74, 75, 87, 88, 89, 90, 92, 109], 'location': 'B', 'alleys': ['XX', 'XZ']}, 
        92: {'adjacent': [75, 76, 77, 90, 91, 93, 109], 'location': 'B', 'alleys': ['XX', 'XY']}, 
        93: {'adjacent': [75, 76, 77, 90, 92, 94, 108, 109, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XY', 'XF']}, 
        94: {'adjacent': [79, 93, 95, 108, 109, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XF']}, 
        95: {'adjacent': [79, 94], 'location': 'H4', 'alleys': [' ']}, 
        96: {'adjacent': [97, 98, 113, 114, 115, 116], 'location': 'H4', 'alleys': [' ']}, 
        97: {'adjacent': [46, 64, 65, 79, 80, 96, 98, 113, 114, 115, 116], 'location': 'B', 'alleys': [' ']}, 
        98: {'adjacent': [96, 97, 113, 114, 115, 116], 'location': 'H5', 'alleys': [' ']}, 
        99: {'adjacent': [68, 69, 81, 82, 100, 101, 117, 118], 'location': 'B', 'alleys': ['XQ', 'XR', 'WA']}, 
        100: {'adjacent': [83, 85, 99, 101, 102, 103, 118, 119], 'location': 'B', 'alleys': ['WB', 'WC', 'WI']}, 
        101: {'adjacent': [70, 82, 83, 84, 85, 99, 100, 103, 118], 'location': 'B', 'alleys': ['XR', 'XS', 'WB']}, 
        102: {'adjacent': [100, 103, 119], 'location': 'B', 'alleys': ['WC', 'WD']}, 
        103: {'adjacent': [83, 85, 100, 101, 102], 'location': 'B', 'alleys': ['WC', 'WD']}, 
        104: {'adjacent': [105, 121, 122, 123], 'location': 'B', 'alleys': ['WD', 'WJ']}, 
        105: {'adjacent': [86, 88, 89, 104, 106, 123], 'location': 'B', 'alleys': ['WD', 'WE', 'WK']}, 
        106: {'adjacent': [89, 105, 107, 126, 127], 'location': 'B', 'alleys': ['WK', 'WF']}, 
        107: {'adjacent': [89, 106, 108, 126, 127, 128], 'location': 'B', 'alleys': ['WF', 'WG', 'WL']}, 
        108: {'adjacent': [89, 93, 94, 107, 109, 110, 111, 112, 127, 128, 130], 'location': 'B', 'alleys': ['WG', 'XZ', 'WN']}, 
        109: {'adjacent': [91, 92, 93, 94, 108, 110, 111, 112, 130], 'location': 'B', 'alleys': ['XZ', 'XY']}, 
        110: {'adjacent': [93, 94, 108, 109, 111, 112, 130], 'location': 'H3', 'alleys': [' ']}, 
        111: {'adjacent': [93, 94, 108, 109, 110, 112, 130], 'location': 'H4', 'alleys': [' ']}, 
        112: {'adjacent': [93, 94, 108, 109, 110, 111, 114, 130, 131, 132, 145, 147], 'location': 'B', 'alleys': [' ']}, 
        113: {'adjacent': [96, 97, 98, 114, 115, 116], 'location': 'H4', 'alleys': [' ']}, 
        114: {'adjacent': [96, 97, 98, 112, 113, 115, 116, 131, 132, 145, 147], 'location': 'B', 'alleys': ['WO']}, 
        115: {'adjacent': [96, 97, 98, 113, 114, 116, 133], 'location': 'B', 'alleys': ['WO', 'WH']}, 
        116: {'adjacent': [96, 97, 98, 113, 114, 115, 133], 'location': 'B', 'alleys': ['WH']}, 
        117: {'adjacent': [81, 99, 118, 134], 'location': 'W3', 'alleys': ['WI']}, 
        118: {'adjacent': [81, 99, 100, 101, 117], 'location': 'B', 'alleys': ['WA', 'WI']}, 
        119: {'adjacent': [100, 102, 121, 134], 'location': 'W3', 'alleys': ['WI', 'WD']}, 
        120: {'adjacent': [135, 139, 153, 155], 'location': 'W3', 'alleys': ['WP', 'WU']}, 
        121: {'adjacent': [104, 119, 122, 134], 'location': 'W3', 'alleys': ['WP', 'WD']}, 
        122: {'adjacent': [104, 121, 123, 124, 139, 140, 161, 162], 'location': 'W3', 'alleys': ['WP', 'WJ', 'WQ']}, 
        123: {'adjacent': [104, 105, 122, 124], 'location': 'W3', 'alleys': ['WJ', 'WK']}, 
        124: {'adjacent': [122, 123, 125], 'location': 'B', 'alleys': ['WK', 'WQ']}, 
        125: {'adjacent': [124, 126, 140, 141], 'location': 'B', 'alleys': ['WK', 'WQ']}, 
        126: {'adjacent': [106, 107, 125, 127, 128, 129, 140, 141], 'location': 'B', 'alleys': ['WK', 'WM', 'WR']}, 
        127: {'adjacent': [106, 107, 108, 126, 128], 'location': 'B', 'alleys': ['WM', 'WL']}, 
        128: {'adjacent': [107, 108, 126, 127, 129], 'location': 'B', 'alleys': ['WM', 'WN']}, 
        129: {'adjacent': [126, 128, 130, 142, 143], 'location': 'W4', 'alleys': ['WN', 'WR']}, 
        130: {'adjacent': [93, 94, 108, 109, 110, 111, 112, 129, 142, 143], 'location': 'W4', 'alleys': ['WN']}, 
        131: {'adjacent': [112, 114, 132, 145, 147], 'location': 'H3', 'alleys': [' ']}, 
        132: {'adjacent': [112, 114, 131, 133, 145, 147, 149], 'location': 'W4', 'alleys': ['WO', 'WS']}, 
        133: {'adjacent': [115, 116, 132, 149, 151], 'location': 'W4', 'alleys': ['WO', 'WT']}, 
        134: {'adjacent': [117, 119, 120, 121, 135, 153, 155], 'location': 'W3', 'alleys': ['WI', 'WP']}, 
        135: {'adjacent': [120, 134, 136, 137, 153, 155], 'location': 'W3', 'alleys': ['WU', 'WY']}, 
        136: {'adjacent': [135, 137, 156, 158], 'location': 'W3', 'alleys': ['WY']}, 
        137: {'adjacent': [135, 136, 138, 139], 'location': 'W3', 'alleys': ['WU']}, 
        138: {'adjacent': [137, 139], 'location': 'H2', 'alleys': [' ']}, 
        139: {'adjacent': [120, 122, 137, 138, 140, 160, 161, 162], 'location': 'W3', 'alleys': ['WU', 'WP']}, 
        140: {'adjacent': [122, 125, 126, 139, 141, 161, 162], 'location': 'B', 'alleys': ['WQ', 'WV']}, 
        141: {'adjacent': [125, 126, 140, 162, 164], 'location': 'B', 'alleys': ['WV', 'WR']}, 
        142: {'adjacent': [129, 130, 143, 165, 166], 'location': 'W4', 'alleys': ['WR']}, 
        143: {'adjacent': [129, 130, 142], 'location': 'H3', 'alleys': [' ']}, 
        144: {'adjacent': [145, 146, 168], 'location': 'H3', 'alleys': [' ']}, 
        145: {'adjacent': [112, 114, 131, 132, 144, 146, 147, 168], 'location': 'W4', 'alleys': ['WW']}, 
        146: {'adjacent': [144, 145, 148, 168, 169, 170], 'location': 'W4', 'alleys': ['WW', 'VA']}, 
        147: {'adjacent': [112, 114, 131, 132, 145, 148, 149, 150], 'location': 'W4', 'alleys': ['WS', 'WW']}, 
        148: {'adjacent': [146, 147, 149, 150, 169, 170], 'location': 'W4', 'alleys': ['WW', 'WX']}, 
        149: {'adjacent': [132, 133, 147, 148, 150], 'location': 'W4', 'alleys': ['WS', 'WT']}, 
        150: {'adjacent': [147, 148, 149, 151, 172], 'location': 'W4', 'alleys': ['WT', 'WX']}, 
        151: {'adjacent': [133, 150, 172], 'location': 'W4', 'alleys': ['WT']}, 
        152: {'adjacent': [153, 154], 'location': 'W3', 'alleys': [' ']}, 
        153: {'adjacent': [120, 134, 135, 152, 155], 'location': 'W3', 'alleys': [' ']}, 
        154: {'adjacent': [152, 155, 156, 157, 159, 174, 175], 'location': 'H1', 'alleys': [' ']}, 
        155: {'adjacent': [120, 134, 135, 153, 154, 156, 157, 159, 174, 175], 'location': 'W3', 'alleys': ['WY']}, 
        156: {'adjacent': [136, 154, 155, 157, 158, 159, 174, 175], 'location': 'W3', 'alleys': ['WY']}, 
        157: {'adjacent': [154, 155, 156, 159, 174, 175], 'location': 'H2', 'alleys': [' ']}, 
        158: {'adjacent': [136, 156], 'location': 'H2', 'alleys': [' ']}, 
        159: {'adjacent': [154, 155, 156, 157, 160, 174, 175, 177], 'location': 'W3', 'alleys': ['VC']}, 
        160: {'adjacent': [139, 159, 177], 'location': 'H2', 'alleys': [' ']}, 
        161: {'adjacent': [122, 139, 140, 162, 163, 176, 177, 178, 179], 'location': 'W3', 'alleys': ['VD', 'WZ']}, 
        162: {'adjacent': [122, 139, 140, 141, 161, 164], 'location': 'B', 'alleys': ['WV', 'WZ']}, 
        163: {'adjacent': [161, 164, 178, 180, 181], 'location': 'B', 'alleys': ['WZ', 'VE']}, 
        164: {'adjacent': [141, 162, 163, 180, 181], 'location': 'B', 'alleys': ['WZ', 'WR']}, 
        165: {'adjacent': [142, 166, 181, 183, 184], 'location': 'W4', 'alleys': ['WR']}, 
        166: {'adjacent': [142, 165], 'location': 'H3', 'alleys': [' ']}, 
        167: {'adjacent': [168, 186], 'location': 'H3', 'alleys': [' ']}, 
        168: {'adjacent': [144, 145, 146, 167, 186], 'location': 'W4', 'alleys': ['VA']}, 
        169: {'adjacent': [146, 148, 170, 171, 187, 188], 'location': 'W4', 'alleys': ['VA', 'VB']}, 
        170: {'adjacent': [146, 148, 169, 171, 172], 'location': 'W4', 'alleys': ['WX', 'VB']}, 
        171: {'adjacent': [169, 170, 172, 187, 188], 'location': 'W4', 'alleys': ['VB']}, 
        172: {'adjacent': [150, 151, 170, 171], 'location': 'W4', 'alleys': ['WX']}, 
        173: {'adjacent': [174, 175, 189], 'location': 'W3', 'alleys': ['VH']}, 
        174: {'adjacent': [154, 155, 156, 157, 159, 173, 175], 'location': 'H1', 'alleys': [' ']}, 
        175: {'adjacent': [154, 155, 156, 157, 159, 173, 174, 176, 177, 189], 'location': 'W3', 'alleys': ['VC', 'VH', 'VI']}, 
        176: {'adjacent': [161, 175, 178, 179, 189], 'location': 'W3', 'alleys': ['VI']}, 
        177: {'adjacent': [159, 160, 161, 175, 176, 178, 179], 'location': 'W3', 'alleys': ['VC', 'VI']}, 
        178: {'adjacent': [161, 163, 176, 177, 179], 'location': 'W3', 'alleys': ['VD', 'VE']}, 
        179: {'adjacent': [161, 176, 177, 178, 180, 182], 'location': 'B', 'alleys': ['VE']}, 
        180: {'adjacent': [163, 164, 179, 181, 182], 'location': 'B', 'alleys': ['VE', 'VF']}, 
        181: {'adjacent': [163, 164, 165, 180, 183, 184], 'location': 'B', 'alleys': ['WR', 'VF']}, 
        182: {'adjacent': [179, 180, 183, 185], 'location': 'B', 'alleys': ['VF']}, 
        183: {'adjacent': [165, 181, 182, 184, 185], 'location': 'W4', 'alleys': ['VF']}, 
        184: {'adjacent': [165, 181, 183], 'location': 'H3', 'alleys': [' ']}, 
        185: {'adjacent': [182, 183, 186, 187, 188], 'location': 'W4', 'alleys': [' ']}, 
        186: {'adjacent': [167, 168, 185, 187, 188], 'location': 'W4', 'alleys': ['VA']}, 
        187: {'adjacent': [169, 171, 185, 186, 188], 'location': 'W4', 'alleys': ['VA', 'VG']}, 
        188: {'adjacent': [169, 171, 185, 186, 187], 'location': 'W4', 'alleys': ['VG']}, 
        189: {'adjacent': [173, 175, 176], 'location': 'W3', 'alleys': ['VH']}}

    # INVESTIGATOR_DICT contains information relevant to the investigator's movements
    # keys correspond to the manually labeled squares investigators can occupy
    # 'adj squares': investigator squares adjacent to the key
    # 'adj circles': Jack's circles adjacent to the key
    # Note: keys of length 3 correspond to allowed starting locations for investigators
    INVESTIGATOR_DICT = {'HA': {'adj squares': ['HB', 'HR', 'HQ'], 'adj circles': [1, 8, 9]}, 
        'HB': {'adj squares': ['HA', 'HC', 'HS'], 'adj circles': [1, 9, 11]}, 
        'HC': {'adj squares': ['HB', 'HD', 'HT'], 'adj circles': [12]}, 
        'HD': {'adj squares': ['HE', 'HF', 'HU', 'HC'], 'adj circles': [2, 14]}, 
        'HE': {'adj squares': ['HD', 'HF', 'HG'], 'adj circles': [2]}, 
        'HF': {'adj squares': ['HD', 'HE', 'HG', 'HU'], 'adj circles': [2, 16]}, 
        'HG': {'adj squares': ['HE', 'HF', 'HU', 'HH', 'HV', 'HI'], 'adj circles': [16, 17, 3]}, 
        'HH': {'adj squares': ['HG', 'HI', 'HV', 'HW'], 'adj circles': [3, 18]}, 
        'HI': {'adj squares': ['HG', 'HH', 'HJ', 'HX', 'HY'], 'adj circles': [3, 4]}, 
        'HJ': {'adj squares': ['HI', 'HK', 'HY', 'HZ'], 'adj circles': [4, 5, 20]}, 
        'HK': {'adj squares': ['HJ', 'HL', 'HZ', 'AA'], 'adj circles': [5, 22, 23]}, 
        'HL': {'adj squares': ['HK', 'HM', 'AB', 'AA', 'AL', 'AK'], 'adj circles': [23, 6, 24]}, 
        'HM': {'adj squares': ['HL', 'HN', 'HO', 'AB'], 'adj circles': [6, 25]}, 
        'HN': {'adj squares': ['HM', 'HO', 'HP'], 'adj circles': [7, 25]}, 
        'HO': {'adj squares': ['HM', 'HN', 'HP', 'AB', 'AM'], 'adj circles': [25, 45]}, 
        'HP': {'adj squares': ['HN', 'HO', 'AC', 'AM'], 'adj circles': [7, 26, 27]}, 
        'HQ': {'adj squares': ['HA', 'HR', 'AN'], 'adj circles': [8, 28]}, 
        'HR': {'adj squares': ['HA', 'HQ', 'AD', 'HS'], 'adj circles': [10, 29]}, 
        'HS': {'adj squares': ['HR', 'HB', 'AE'], 'adj circles': [10, 11]}, 
        'HT': {'adj squares': ['HC', 'HD', 'HU', 'AF'], 'adj circles': [12, 13, 14]}, 
        'HU': {'adj squares': ['HT', 'AF', 'HD', 'AG', 'HF', 'HG'], 'adj circles': [13, 14, 15, 16]}, 
        'HV': {'adj squares': ['HG', 'HH', 'AG', 'AH'], 'adj circles': [17, 18]}, 
        'HW': {'adj squares': ['HH', 'HX', 'AH', 'AS', 'AT'], 'adj circles': [19, 37]}, 
        'HX': {'adj squares': ['HI', 'HW', 'HY', 'AT'], 'adj circles': [19, 38]}, 
        'HY': {'adj squares': ['HI', 'HX', 'HJ', 'HZ', 'AI'], 'adj circles': [20, 21]}, 
        'HZ': {'adj squares': ['HY', 'HJ', 'HK', 'AA', 'AI'], 'adj circles': [20, 21, 22]}, 
        'AA': {'adj squares': ['HZ', 'HK', 'HL', 'AJ', 'AI'], 'adj circles': [22, 23, 41]}, 
        'AB': {'adj squares': ['HM', 'HL', 'HO', 'AK', 'AL', 'AM'], 'adj circles': [24, 45]}, 
        'AC': {'adj squares': ['HP', 'AM', 'AY'], 'adj circles': [26, 27, 47]}, 
        'AD': {'adj squares': ['HR', 'AN', 'AE', 'AO'], 'adj circles': [29, 30, 31]}, 
        'AE': {'adj squares': ['HS', 'AD', 'HT', 'HU', 'AF', 'AP'], 'adj circles': [13, 32]}, 
        'AF': {'adj squares': ['HT', 'HU', 'AE', 'AG', 'AP', 'AQ'], 'adj circles': [13, 33]}, 
        'AG': {'adj squares': ['HU', 'HV', 'AF', 'AP', 'AQ', 'AH'], 'adj circles': [15, 33, 34]}, 
        'AH': {'adj squares': ['AV', 'HW', 'AG', 'AQ', 'AT', 'AS', 'AR'], 'adj circles': [34, 35, 37]}, 
        'AI': {'adj squares': ['HY', 'HZ', 'AA', 'AT'], 'adj circles': [21, 41]}, 
        'AJ': {'adj squares': ['AA', 'AK', 'AU', 'AV'], 'adj circles': [42]}, 
        'AK': {'adj squares': ['AJ', 'HL', 'AB', 'AL'], 'adj circles': [24, 44]}, 
        'AL': {'adj squares': ['HL', 'AK', 'AB', 'AM', 'AW', 'AX', 'BI'], 'adj circles': [24, 46]}, 
        'AM': {'adj squares': ['AB', 'HO', 'HP', 'AC', 'AX', 'BI'], 'adj circles': [45, 46, 26]}, 
        'AN': {'adj squares': ['HQ', 'AD', 'AZ', 'BA'], 'adj circles': [28, 48, 30]}, 
        'AO': {'adj squares': ['AD', 'BA', 'BL', 'BB', 'AP'], 'adj circles': [31, 51]}, 
        'AP': {'adj squares': ['AO', 'AE', 'AF', 'AG', 'AQ', 'BB', 'BC'], 'adj circles': [32, 33, 53]}, 
        'AQ': {'adj squares': ['AP', 'AF', 'AG', 'AR', 'AH', 'BC'], 'adj circles': [33, 34, 54]}, 
        'AR': {'adj squares': ['AQ', 'BD', 'AH', 'AS'], 'adj circles': [35, 54]}, 
        'AS': {'adj squares': ['AH', 'AR', 'BD', 'BM', 'HW', 'AT', 'BE'], 'adj circles': [36, 37, 56]}, 
        'AT': {'adj squares': ['HW', 'AH', 'AS', 'HX', 'AI', 'AU', 'BE', 'BF'], 'adj circles': [37, 38, 39, 40]}, 
        'AU': {'adj squares': ['AT', 'BF', 'BG', 'AV', 'AJ'], 'adj circles': [40, 42, 59]}, 
        'AV': {'adj squares': ['AU', 'AJ', 'AK', 'BG', 'AW', 'BH'], 'adj circles': [42, 43, 44, 59]}, 
        'AW': {'adj squares': ['AV', 'AL', 'BG', 'BH', 'AV'], 'adj circles': [43, 44]}, 
        'AX': {'adj squares': ['AL', 'AM', 'BH', 'BX', 'BI'], 'adj circles': [46, 62, 63]}, 
        'AY': {'adj squares': ['AC', 'BI', 'BJ'], 'adj circles': [47, 65, 67]}, 
        'AZ': {'adj squares': ['AN', 'BA', 'BK'], 'adj circles': [48, 49]}, 
        'BA': {'adj squares': ['AZ', 'AN', 'AO', 'BK', 'BO', 'BL', 'BB'], 'adj circles': [49, 50, 51]}, 
        'BB': {'adj squares': ['BA', 'AO', 'AP', 'BC', 'BL', 'BP', 'BQ'], 'adj circles': [51, 52, 53]}, 
        'BC': {'adj squares': ['BB', 'AP', 'BD', 'AQ', 'BQ', 'BR'], 'adj circles': [53, 54, 55]}, 
        'BD': {'adj squares': ['AR', 'BC', 'AS', 'BS'], 'adj circles': [36]}, 
        'BE': {'adj squares': ['AS', 'AT', 'BF', 'BM', 'BT'], 'adj circles': [39, 56, 57]}, 
        'BF': {'adj squares': ['BE', 'AU', 'BU', 'BG'], 'adj circles': [58]}, 
        'BG': {'adj squares': ['BU', 'BF', 'AU', 'AV', 'AW', 'BH', 'BV'], 'adj circles': [58, 59, 43]}, 
        'BH': {'adj squares': ['BG', 'AV', 'AW', 'AX', 'BX', 'BV', 'BW'], 'adj circles': [43, 60, 61, 62]}, 
        'BI': {'adj squares': ['AX', 'AL', 'AM', 'AY', 'BY'], 'adj circles': [46, 65]}, 
        'BJ': {'adj squares': ['AY', 'BY'], 'adj circles': [64, 66, 67]}, 
        'BK': {'adj squares': ['AZ', 'BA', 'BN', 'BO'], 'adj circles': [50]}, 
        'BL': {'adj squares': ['BO', 'BA', 'AO', 'BB', 'BP'], 'adj circles': [51]}, 
        'BM': {'adj squares': ['AS', 'BE', 'BS', 'BT'], 'adj circles': [56, 73]}, 
        'BN': {'adj squares': ['BK', 'BO', 'CA'], 'adj circles': [68]}, 
        'BO': {'adj squares': ['CA', 'BN', 'BK', 'BA', 'BL', 'BP'], 'adj circles': [50, 68, 69]}, 
        'BP': {'adj squares': ['CA', 'BO', 'BL', 'BB', 'BQ', 'CI'], 'adj circles': [52, 69, 70]}, 
        'BQ': {'adj squares': ['BP', 'BB', 'BC', 'BR', 'CB'], 'adj circles': [52, 55, 71]}, 
        'BR': {'adj squares': ['CB', 'BQ', 'BC', 'BS', 'CC'], 'adj circles': [55, 71, 72]}, 
        'BS': {'adj squares': ['CC', 'BR', 'BD', 'BM', 'BT'], 'adj circles': [72, 73]}, 
        'BT': {'adj squares': ['BS', 'BM', 'BE', 'BU', 'CD'], 'adj circles': [57, 73, 74]}, 
        'BU': {'adj squares': ['BT', 'BF', 'BG', 'BV', 'CD', 'CL', 'CE'], 'adj circles': [58, 75, 76]}, 
        'BV': {'adj squares': ['CE', 'BU', 'BG', 'BH', 'BW', 'CM'], 'adj circles': [60, 76]},
        'BW': {'adj squares': ['CM', 'BBB', 'BV'], 'adj circles': [77, 78]},  
        'BX': {'adj squares': ['BH', 'AX'], 'adj circles': [61, 63]}, 
        'BY': {'adj squares': ['BI', 'BJ', 'BZ', 'CO'], 'adj circles': [64, 97]}, 
        'BZ': {'adj squares': ['BY', 'CF'], 'adj circles': [79, 80]}, 
        'CA': {'adj squares': ['BN', 'BO', 'BP', 'CG'], 'adj circles': [68, 69, 81]}, 
        'CB': {'adj squares': ['BQ', 'BR', 'CJ', 'CI'], 'adj circles': [71, 84]}, 
        'CC': {'adj squares': ['BR', 'BS', 'CJ', 'AAA'], 'adj circles': [72, 87]}, 
        'CD': {'adj squares': ['AAA', 'BT', 'CK', 'CL'], 'adj circles': [74, 75]}, 
        'CE': {'adj squares': ['CL', 'BU', 'BV', 'BBB'], 'adj circles': [76]}, 
        'CF': {'adj squares': ['BZ', 'CN'], 'adj circles': [79, 94, 95]}, 
        'CG': {'adj squares': ['CA', 'CH', 'CP', 'CQ'], 'adj circles': [82, 99]}, 
        'CH': {'adj squares': ['CG', 'CI', 'CQ', 'CR'], 'adj circles': [82, 101]}, 
        'CI': {'adj squares': ['CH', 'BP', 'CB', 'CS'], 'adj circles': [70, 83, 84]}, 
        'CJ': {'adj squares': ['CS', 'CB', 'CC', 'AAA', 'CCC'], 'adj circles': [85, 86, 87]}, 
        'CK': {'adj squares': ['CD', 'CL', 'CT', 'CU', 'CCC'], 'adj circles': [89, 90, 91]}, 
        'CL': {'adj squares': ['CD', 'CE', 'CK', 'DDD', 'BU'], 'adj circles': [75, 90, 92]}, 
        'CM': {'adj squares': ['BW', 'BBB'], 'adj circles': [77, 78]}, 
        'CN': {'adj squares': ['CF', 'CV'], 'adj circles': [94, 111]}, 
        'CO': {'adj squares': ['BY', 'CW', 'DD'], 'adj circles': [97, 98, 116]}, 
        'CP': {'adj squares': ['CA', 'CG', 'CQ', 'CX'], 'adj circles': [81, 99]}, 
        'CQ': {'adj squares': ['CG', 'CP', 'CH', 'CR', 'CY'], 'adj circles': [99, 101]}, 
        'CR': {'adj squares': ['CH', 'CQ', 'CY', 'CS', 'DE'], 'adj circles': [100, 101]}, 
        'CS': {'adj squares': ['CR', 'CI', 'CJ', 'CZ'], 'adj circles': [83, 85, 103]}, 
        'CT': {'adj squares': ['CK', 'CU', 'CCC', 'EEE', 'FFF'], 'adj circles': [89, 105, 106]}, 
        'CU': {'adj squares': ['CK', 'CT', 'DB', 'DA', 'CCC', 'FFF', 'DH'], 'adj circles': [89, 107, 108]}, 
        'CV': {'adj squares': ['CN', 'DB', 'DI', 'BBB', 'DDD'], 'adj circles': [93, 109, 112]}, 
        'CW': {'adj squares': ['CO', 'DC'], 'adj circles': [96]}, 
        'CX': {'adj squares': ['CP', 'CY', 'DJ'], 'adj circles': [117, 118]}, 
        'CY': {'adj squares': ['CX', 'CQ', 'CR', 'DE'], 'adj circles': [118, 100]}, 
        'CZ': {'adj squares': ['CS', 'DE'], 'adj circles': [102, 103]}, 
        'DA': {'adj squares': ['DH', 'DB', 'CU', 'DO'], 'adj circles': [108, 128]}, 
        'DB': {'adj squares': ['DA', 'CU', 'CV', 'DP'], 'adj circles': [108, 110, 130]}, 
        'DC': {'adj squares': ['CW', 'DD', 'DI'], 'adj circles': [113, 114, 115]}, 
        'DD': {'adj squares': ['CO', 'DC', 'DS', 'DR'], 'adj circles': [115, 116, 133]}, 
        'DE': {'adj squares': ['CY', 'CR', 'CZ', 'DK'], 'adj circles': [100, 102, 119]}, 
        'DF': {'adj squares': ['DM', 'DK', 'DV', 'EEE'], 'adj circles': [104, 121, 122]}, 
        'DG': {'adj squares': ['DH', 'DO', 'EE', 'FFF'], 'adj circles': [126, 127]}, 
        'DH': {'adj squares': ['DG', 'DA', 'CU', 'FFF'], 'adj circles': [107, 127]}, 
        'DI': {'adj squares': ['CV', 'DC', 'DR', 'DQ'], 'adj circles': [114, 112, 132]}, 
        'DJ': {'adj squares': ['CX', 'DK', 'EA'], 'adj circles': [117, 134]}, 
        'DK': {'adj squares': ['DJ', 'EA', 'DE', 'DF'], 'adj circles': [119, 121, 134]}, 
        'DL': {'adj squares': ['DT', 'DV', 'DU'], 'adj circles': [120, 139]}, 
        'DM': {'adj squares': ['DF', 'DV', 'DN', 'EEE'], 'adj circles': [122, 123, 124]}, 
        'DN': {'adj squares': ['DM', 'ED'], 'adj circles': [124, 125]}, 
        'DO': {'adj squares': ['DA', 'DG', 'DP', 'EE'], 'adj circles': [126, 128, 129]}, 
        'DP': {'adj squares': ['DO', 'DW', 'DB'], 'adj circles': [129, 130]}, 
        'DQ': {'adj squares': ['DI', 'DX'], 'adj circles': [131]}, 
        'DR': {'adj squares': ['DI', 'DD', 'DS', 'DY'], 'adj circles': [132, 133, 149]}, 
        'DS': {'adj squares': ['DD', 'DR', 'DZ'], 'adj circles': [133, 151]}, 
        'DT': {'adj squares': ['EA', 'DL'], 'adj circles': [120]}, 
        'DU': {'adj squares': ['EB', 'DL', 'DV', 'EL'], 'adj circles': [137, 138, 139]}, 
        'DV': {'adj squares': ['DU', 'DL', 'EL', 'DF', 'DM', 'EC'], 'adj circles': [139, 122]}, 
        'DW': {'adj squares': ['DP', 'EF'], 'adj circles': [142, 143]}, 
        'DX': {'adj squares': ['DQ', 'DY', 'EG'], 'adj circles': [145, 147]}, 
        'DY': {'adj squares': ['DX', 'DR', 'DZ', 'EH'], 'adj circles': [147, 148, 149, 150]}, 
        'DZ': {'adj squares': ['DY', 'DS', 'EP'], 'adj circles': [150, 151, 172]}, 
        'EA': {'adj squares': ['DJ', 'DK', 'DT', 'EB', 'EI', 'EJ'], 'adj circles': [134, 135, 153, 155]}, 
        'EB': {'adj squares': ['EA', 'EK', 'DU'], 'adj circles': [135, 136, 137]}, 
        'EC': {'adj squares': ['DV', 'ED', 'EM'], 'adj circles': [140]}, 
        'ED': {'adj squares': ['EC', 'DN', 'EE'], 'adj circles': [140, 125]}, 
        'EE': {'adj squares': ['ED', 'DG', 'DO', 'EN'], 'adj circles': [126, 141]}, 
        'EF': {'adj squares': ['DW', 'EX'], 'adj circles': [142, 165, 166]}, 
        'EG': {'adj squares': ['DX', 'EH', 'EY'], 'adj circles': [144, 145, 146, 168]}, 
        'EH': {'adj squares': ['EG', 'DY', 'EO'], 'adj circles': [146, 148]}, 
        'EI': {'adj squares': ['EA', 'EQ'], 'adj circles': [152, 153]}, 
        'EJ': {'adj squares': ['EA', 'EQ', 'EK', 'ER'], 'adj circles': [154, 155, 156]}, 
        'EK': {'adj squares': ['EJ', 'EB'], 'adj circles': [156, 158, 136]}, 
        'EL': {'adj squares': ['DL', 'DU', 'DV', 'EU'], 'adj circles': [160, 139]}, 
        'EM': {'adj squares': ['EC', 'EN', 'EV', 'FG'], 'adj circles': [161, 162]}, 
        'EN': {'adj squares': ['EM', 'EE', 'EW'], 'adj circles': [141, 162, 164]}, 
        'EO': {'adj squares': ['EH', 'EP', 'EZ'], 'adj circles': [169, 170]}, 
        'EP': {'adj squares': ['DZ', 'EO', 'FA'], 'adj circles': [170, 171, 172]}, 
        'EQ': {'adj squares': ['EI', 'EJ'], 'adj circles': [152, 154]}, 
        'ER': {'adj squares': ['EJ', 'ES', 'FB', 'FC', 'FD', 'FF'], 'adj circles': [174, 175]}, 
        'ES': {'adj squares': ['ER', 'ET', 'FC', 'FD', 'FF'], 'adj circles': [157, 159, 175]}, 
        'ET': {'adj squares': ['ES', 'EU', 'FD', 'FG'], 'adj circles': [159, 177]}, 
        'EU': {'adj squares': ['EL', 'ET', 'FD', 'FG'], 'adj circles': [160, 177]}, 
        'EV': {'adj squares': ['EM', 'FG', 'FH', 'EW'], 'adj circles': [161, 163, 178]}, 
        'EW': {'adj squares': ['EV', 'EN', 'FI', 'EX'], 'adj circles': [163, 164, 180, 181]}, 
        'EX': {'adj squares': ['EW', 'EF', 'FJ'], 'adj circles': [165, 181, 183, 184]}, 
        'EY': {'adj squares': ['EG', 'FK'], 'adj circles': [167, 168, 186]}, 
        'EZ': {'adj squares': ['EO', 'FA', 'FL'], 'adj circles': [169, 187]}, 
        'FA': {'adj squares': ['EP', 'EZ', 'FL'], 'adj circles': [171, 188]}, 
        'FB': {'adj squares': ['ER', 'FC', 'FE'], 'adj circles': [173, 174]}, 
        'FC': {'adj squares': ['FB', 'FE', 'ER', 'ES', 'FD', 'FF'], 'adj circles': [173, 175]}, 
        'FD': {'adj squares': ['ER', 'ES', 'ET', 'FC', 'FF', 'FG'], 'adj circles': [175, 177]}, 
        'FE': {'adj squares': ['FB', 'FC', 'FF'], 'adj circles': [173, 189]}, 
        'FF': {'adj squares': ['FE', 'FC', 'ER', 'ES', 'FD', 'FG'], 'adj circles': [189, 175, 176]}, 
        'FG': {'adj squares': ['FF', 'FD', 'ET', 'EU', 'EM', 'EV', 'FH'], 'adj circles': [176, 177, 161]}, 
        'FH': {'adj squares': ['FG', 'EV', 'FI'], 'adj circles': [178, 179]}, 
        'FI': {'adj squares': ['FH', 'EW', 'FJ'], 'adj circles': [179, 180, 182]}, 
        'FJ': {'adj squares': ['FI', 'EX', 'FK'], 'adj circles': [182, 183, 185]}, 
        'FK': {'adj squares': ['FJ', 'EY', 'FL'], 'adj circles': [185, 186]}, 
        'FL': {'adj squares': ['FK', 'EZ', 'FA'], 'adj circles': [187, 188]},
        'AAA': {'adj squares': ['CJ', 'CC', 'CD', 'CCC'], 'adj circles': [87, 88]},
        'BBB': {'adj squares': ['CL', 'CE', 'CM', 'CV', 'DDD', 'BW'], 'adj circles': [92, 93, 77]}, 
        'CCC': {'adj squares': ['AAA', 'CJ', 'EEE', 'CT', 'CK', 'CU'], 'adj circles': [86, 88, 89, 105]}, 
        'DDD': {'adj squares': ['BBB', 'CL', 'CV', 'CK'], 'adj circles': [91, 92, 109]}, 
        'EEE': {'adj squares': ['CCC', 'CT', 'DF', 'DM'], 'adj circles': [104, 105, 123]}, 
        'FFF': {'adj squares': ['CT', 'CU', 'DG', 'DH'], 'adj circles':[106, 107]}}

    # Dictionaries for each of the four white circle quadrants
    W1, W2, W3, W4 = quads(JACK_DICT)

    SPECIAL_MOVEMENTS = {'coach':{'int':1, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0},
     'alley':{'int':2, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0}, 
     'boat':{'int':3, 'remaining':2, 'first use round/turn':0, 'second use round/turn':0}}

    # begin the game
    print("Welcome to Whitehall Mystery!")
    print("Get ready to go head to head with Jack the AI!")
    DISCOVERY_LOCATIONS = pick_DL(W1, W2, W3, W4)        # Jack picks Discovery Locations
    print("Jack has picked his Discovery Locations")
    jack_loc = pick_loc(DISCOVERY_LOCATIONS)                        # Jack picks starting location from Discovery Locations
    COPY_OF_DISCOVERY_LOCATIONS = DISCOVERY_LOCATIONS
    COPY_OF_DISCOVERY_LOCATIONS.remove(jack_loc)
    goal_loc = pick_loc(COPY_OF_DISCOVERY_LOCATIONS)
    INVESTIGATOR_LOCATIONS = input_investigator_loc()                                   # The Investigators input their starting locations
    print(f"Jack: I'm at my starting location, {jack_loc}. Come and get me!")
    print(f"Jack's goal for his next location is: {goal_loc}")

    round = 0             # iterator to keep track of the round (out of 4 rounds)
    turn = 0              # iterator to keep track of the turn (15 turns for each round)
    jack_win = 1          # boolean to keep track if Jack is winning
    CLUES = []
    JACK_LOCATIONS = []
    while round < 5:
        round, turn, CLUES, JACK_LOCATIONS = next_round(round, turn, CLUES, JACK_LOCATIONS)
        JACK_LOCATIONS.append(jack_loc)
        print(f"Round {round}")
        while turn <= 15:
            turn += 1
            # Jack: Escape the Night
            # TODO: add functionality for special movements, if desired
            jack_loc = jack_move(jack_loc, JACK_DICT, goal_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT) # TODO: add inputs for AI for movement
            print(f"Jack has moved to: {jack_loc}")
            JACK_LOCATIONS.append(jack_loc)
            print("Jack has moved")
            at_goal = check_DL(jack_loc, COPY_OF_DISCOVERY_LOCATIONS)
            if at_goal:
                print("Jack has reached a Discovery Location.")
                COPY_OF_DISCOVERY_LOCATIONS.remove(jack_loc)
                print(f"Jack:'I'm at {jack_loc}, come and get me!")
                break  
            else:
                # Investigators: Hunting the Monster
                # Yellow move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[0], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                # Blue move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[1], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                # Red move
                INVESTIGATOR_LOCATIONS = investigator_move(INVESTIGATOR_LOCATIONS[2], INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)

                # Investigators: Clues and Suspicion
                # Yellow investigate
                print("Jasper T.C. Waring (yellow):")
                yellow_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if yellow_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[0], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif yellow_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[0], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
                # Blue investigate
                print("Arthur Ferris (blue):")
                blue_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if blue_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[1], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif blue_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[1], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
                # Red investigate
                print("Thomas Bond (red):")
                red_action = int(input("Type 0 if you would like to do nothing, 1 if you would like to look for clues, or 2 if you would like to make an arrest"))
                if red_action == 1:
                    CLUES = look_for_clues(CLUES, INVESTIGATOR_LOCATIONS[2], JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                elif red_action == 2:
                    jack_win = execute_arrest(INVESTIGATOR_LOCATIONS[2], jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT)
                    if jack_win == 0:
                        break
        if jack_win == 0:
            print("Congratulations, investigators, you have won!")
            return jack_win
    print("Jack: Ha ha ha! I have won! Better luck next time, investigators!")
    return jack_win

# helper functions for running the game
def pick_DL(W1, W2, W3, W4):
    """Picks a discovery location from each quadrant of the board.
       Returns a list of discovery locations.
    """
    dl1 = random.choice(list(W1.items()))
    dl1 = dl1[0]
    dl2 = random.choice(list(W2.items()))
    dl2 = dl2[0]
    dl3 = random.choice(list(W3.items()))
    dl3 = dl3[0]
    dl4 = random.choice(list(W4.items()))
    dl4 = dl4[0]
    DL = [dl1, dl2, dl3, dl4]
    return DL

def pick_loc(DL):
    """Returns a random location from the given list."""
    return random.choice(DL)

def input_investigator_loc():
    """Allows investigators to input their locations at the beginning of the game.
       Returns the list of their current locations.
    """
    ALLOWED_STARTING_LOC = ['AAA', 'BBB', 'CCC', 'DDD', 'EEE', 'FFF']

    # input yellow location
    yellow_loc = input("Jasper T.C. Waring (yellow), please select your starting location: ")
    while yellow_loc not in ALLOWED_STARTING_LOC:
        print(f"Jasper (yellow), {yellow_loc} is an invalid starting location, please pick from one of the following starting locations: {ALLOWED_STARTING_LOC}.")
        yellow_loc = input("Jasper T.C. Waring (yellow), please select your starting location: ")

    # input blue location
    blue_loc = input("Arthur Ferris (blue), please select your starting location: ")
    while blue_loc not in ALLOWED_STARTING_LOC:
        print(f"Arthur (blue), {blue_loc} is an invalid starting location, please pick from one of the following starting locations: {ALLOWED_STARTING_LOC}.")
        blue_loc = input("Arthur Ferris (blue), please select your starting location: ")

    # input red location
    red_loc = input("Thomas Bond (red), please select your starting location: ")
    while red_loc not in ALLOWED_STARTING_LOC:
        print(f"Thomas (red), {red_loc} is an invalid starting location, please pick from one of the following starting locations: {ALLOWED_STARTING_LOC}.")
        red_loc = input("Thomas Bond (red), please select your starting location: ")

    INVESTIGATOR_LOCATIONS = [yellow_loc, blue_loc, red_loc]
    return INVESTIGATOR_LOCATIONS

def next_round(round, turn, CLUES, JACK_LOCATIONS):
    """Resets/increments given variables to prepare for the next round."""
    round += 1
    turn = 0
    CLUES = []
    JACK_LOCATIONS = []
    return round, turn, CLUES, JACK_LOCATIONS

def jack_move(jackLoc, J, goal_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
    # TODO: AI
    A = J[jackLoc]['adjacent']
    newLoc = random.choice(A)
    return newLoc

def check_DL(jack_loc, COPY_DISCOVERY_LOC):
    """Checks if Jack's current location is also a discovery location.
       Returns a boolean.
    """
    if jack_loc in COPY_DISCOVERY_LOC:
        return True
    else:
        return False

def investigator_move(current_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
    """Allows investigators to input their movements and
       checks to make sure proposed movements are allowed.
       Returns updated list of investigator locations.
    """
    # yellow moves
    if current_loc == INVESTIGATOR_LOCATIONS[0]:
        print("Jasper (yellow), your turn to move.")
        new_loc = input("Jasper, you move to: ")
        while not investigator_can_move(current_loc, new_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
            print(f"Jasper cannot move to {new_loc} from {current_loc}.")
            new_loc = input("Jasper, please input a valid location to move to: ")
        print(f"Jasper (yellow) has moved from {current_loc} to {new_loc}.")
        INVESTIGATOR_LOCATIONS = [new_loc, INVESTIGATOR_LOCATIONS[1], INVESTIGATOR_LOCATIONS[2]]

    # blue moves
    elif current_loc == INVESTIGATOR_LOCATIONS[1]:
        print("Arthur (blue), your turn to move.")
        new_loc = input("Arthur, you move to: ")
        while not investigator_can_move(current_loc, new_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
            print(f"Arthur cannot move to {new_loc} from {current_loc}.")
            new_loc = input("Arthur, please input a valid location to move to: ")
        print(f"Arthur (blue) has moved from {current_loc} to {new_loc}.")
        INVESTIGATOR_LOCATIONS = [INVESTIGATOR_LOCATIONS[0], new_loc, INVESTIGATOR_LOCATIONS[2]]

    # red moves
    else:
        print("Thomas (red), your turn to move.")
        new_loc = input("Thomas, you move to: ")
        while not investigator_can_move(current_loc, new_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
            print(f"Thomas cannot move to {new_loc} from {current_loc}.")
            new_loc = input("Thomas, please input a valid location to move to: ")
        print(f"Thomas (red) has moved from {current_loc} to {new_loc}.")
        INVESTIGATOR_LOCATIONS = [INVESTIGATOR_LOCATIONS[0], INVESTIGATOR_LOCATIONS[1], new_loc]

    return INVESTIGATOR_LOCATIONS

def investigator_can_move(current_loc, new_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
    """Checks to see if an investigator movement is allowed,
       given the investigator's current location and their
       proposed location
    """
    ADJ1 = INVESTIGATOR_DICT[current_loc]['adj squares']
    ADJ2 = []
    for square1 in ADJ1:
        L = INVESTIGATOR_DICT[square1]['adj squares']
        for square2 in L:
            if square2 not in ADJ2:
                ADJ2.append(square2)
    if current_loc == new_loc:       # move zero spaces
        return True
    elif new_loc in ADJ1 and new_loc not in INVESTIGATOR_LOCATIONS:    # move one space
        return True 
    elif new_loc in ADJ2 and new_loc not in INVESTIGATOR_LOCATIONS:    # move two spaces
        # TODO: keep investigator from moving through another investigator
        return True
    else:
        return False

def look_for_clues(CLUES, current_loc, JACK_LOCATIONS, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
    """Allows investigators to look for clues
       Returns an updated list of clues
       Prints whether a clue has been found
    """
    clue_found = False
    done = False
    while clue_found == False and done == False:
        if current_loc == INVESTIGATOR_LOCATIONS[0]:
            clue_loc = int(input("Jasper (yellow), where would you like to look for clues? "))
            while not clue_loc < 190 or not clue_loc > 0 or not is_adjacent(clue_loc, current_loc, INVESTIGATOR_DICT):
                print("Jasper, you may not look for clues at that location. Please pick a valid location that is:")
                print("An integer less than 190 and greater than 0,")
                print("And is adjacent to your current location.")
                clue_loc = int(input("Jasper (yellow), where would you like to look for clues? "))
            if clue_loc in JACK_LOCATIONS:
                if clue_loc not in CLUES:
                    CLUES.append(clue_loc)
                print(f"Jasper, you have found a clue at {clue_loc}!")
                clue_found = True
            else:
                print(f"Jasper, you have NOT found a clue at {clue_loc}.")
                inp = input("Jasper, type 'yes' if you would like to continue looking for clues or 'no' if you are done: ")
                inp.lower()
                if inp == 'no':
                    done = True
        elif current_loc == INVESTIGATOR_LOCATIONS[1]:
            clue_loc = input("Arthur (blue), where would you like to look for clues? ")
            while not clue_loc < 190 or not clue_loc > 0 or not is_adjacent(clue_loc, current_loc, INVESTIGATOR_DICT):
                print("Arthur, you may not look for clues at that location. Please pick a valid location that is:")
                print("An integer less than 190 and greater than 0,")
                print("And is adjacent to your current location.")
                clue_loc = int(input("Arthur (blue), where would you like to look for clues? "))
            if clue_loc in JACK_LOCATIONS:
                if clue_loc not in CLUES:
                    CLUES.append(clue_loc)
                print(f"Arthur, you have found a clue at {clue_loc}!")
                clue_found = True
            else:
                print(f"Arthur, you have NOT found a clue at {clue_loc}.")
                inp = input("Arthur, type 'yes' if you would like to continue looking for clues or 'no' if you are done: ")
                inp.lower()
                if inp == 'no':
                    done = True
        else:
            clue_loc = input("Thomas (red), where would you like to look for clues? ")
            while not clue_loc < 190 or not clue_loc > 0 or not is_adjacent(clue_loc, current_loc, INVESTIGATOR_DICT):
                print("Thomas, you may not look for clues at that location. Please pick a valid location that is:")
                print("An integer less than 190 and greater than 0,")
                print("And is adjacent to your current location.")
                clue_loc = int(input("Thomas (red), where would you like to look for clues? "))
            if clue_loc in JACK_LOCATIONS:
                if clue_loc not in CLUES:
                    CLUES.append(clue_loc)
                print(f"Thomas, you have found a clue at {clue_loc}!")
                clue_found = True
            else:
                print(f"Thomas, you have NOT found a clue at {clue_loc}.")
                inp = input("Thomas, type 'yes' if you would like to continue looking for clues or 'no' if you are done: ")
                inp.lower()
                if inp == 'no':
                    done = True
    return CLUES

def is_adjacent(loc, current_loc, INVESTIGATOR_DICT):
    """Determines if the given investigator is adjacent
       to a circle (one of Jack's possible location spaces)
    """
    adj_circles = INVESTIGATOR_DICT[current_loc]['adj circles']
    if loc in adj_circles:
        return True
    return False

def execute_arrest(current_loc, jack_loc, INVESTIGATOR_LOCATIONS, INVESTIGATOR_DICT):
    """Allows the current investigator to try
       and make an arrest.
       Returns a boolean to determine who has won:
       0 for investigators, 1 for Jack
    """
    if current_loc == INVESTIGATOR_LOCATIONS[0]:
        arrest_loc = int(input("Jasper (yellow), where would you like to execute an arrest? "))
        while not arrest_loc < 190 or not arrest_loc > 0 or not is_adjacent(arrest_loc, current_loc, INVESTIGATOR_DICT):
            print("Jasper, you may not look for clues at that location. Please pick a valid location that is:")
            print("An integer less than 190 and greater than 0,")
            print("And is adjacent to your current location.")
            arrest_loc = int(input("Jasper (yellow), where would you like to execute an arrest? "))
        if arrest_loc == jack_loc:
            print(f"Jack: Oh no! Jasper, you've found me at {arrest_loc}!")
            return 0
    elif current_loc == INVESTIGATOR_LOCATIONS[1]:
        arrest_loc = int(input("Alfred (blue), where would you like to execute an arrest? "))
        while not arrest_loc < 190 or not arrest_loc > 0 or not is_adjacent(arrest_loc, current_loc, INVESTIGATOR_DICT):
            print("Alfred, you may not look for clues at that location. Please pick a valid location that is:")
            print("An integer less than 190 and greater than 0,")
            print("And is adjacent to your current location.")
            arrest_loc = int(input("Alfred (blue), where would you like to execute an arrest? "))
        if arrest_loc == jack_loc:
            print(f"Jack: Oh no! Alfred, you've found me at {arrest_loc}!")
            return 0
    else:
        arrest_loc = int(input("Thomas (red), where would you like to execute an arrest? "))
        while not arrest_loc < 190 or not arrest_loc > 0 or not is_adjacent(arrest_loc, current_loc, INVESTIGATOR_DICT):
            print("Thomas, you may not look for clues at that location. Please pick a valid location that is:")
            print("An integer less than 190 and greater than 0,")
            print("And is adjacent to your current location.")
            arrest_loc = int(input("Thomas (red), where would you like to execute an arrest? "))
        if arrest_loc == jack_loc:
            print(f"Jack: Oh no! Thomas, you've found me at {arrest_loc}!")
            return 0
    print(f"Jack: Ha ha ha! I'm not at {arrest_loc}!")
    return 1