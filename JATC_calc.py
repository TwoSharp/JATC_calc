import argparse
import math
import sys


#-----------------------------------------------------------------------------------
#                   MISC
#-----------------------------------------------------------------------------------

def _usage(param=None):
    # prints usage page and exits
    print(
        "Usage: JATC_calc.py [option][args]\n"
        " poor mans calculator :')\n\n"
        "[--angle][--side][--radial][--parallel][--convert] [args]]\n"
    )
    if param == "parallel":
        print("--parallel [diameter(in)][elevation height(in)][elevation angle(in)][optional: # of sections]:\n\ttakes arguments in given order and returns stretchout, elevation opposite height, and section width\n")
    else:
        print(
        "--find: use to find a side or angle in a right triangle\n"
        "\tneed at least one angle and one side or two sides\n"
        "--radial [decimal]: use for radial math\n"
        "\tneed top length (diameter), bottom diameter, and taper height\n"
        "\toptional argument [decimal]: output measurements in decimal form\n"
        "\t--convert: use to convert decimal to fraction (only works with inches)\n")

    sys.exit(0)

def num_to_dec(num):
    str_num = str(num)
    if '.' in str_num:
        return num
    elif '/' in str_num:
        num = frac_to_dec(num)
        return num
    else:
        return float(num)

def num_to_frac(num):
    str_num = str(num)
    if '/' in str_num:
        return num
    elif '.' in str_num:
        num = dec_to_frac(num)
        return num
    else:
        return str_num

def dec_to_frac(num):
# takes a decimal and converts it to a fraction
# return type string
    if type(num) != str:
        num = str(num)
    num = num.split('.')

    whole = None
    if num[0]:
        whole = num[0]

    try:
        if num[1]:
            dec = float( '.' + num[1])

            if dec <= 1/16 + 1/32:
                dec = '1/16'
            elif dec <= 1/8 + 1/32:
                dec = '1/8'
            elif dec <= 3/16 + 1/32:
                dec = '3/16'
            elif dec <= 1/4 + 1/32:
                dec = '1/4'
            elif dec <= 5/16 + 1/32:
                dec = '5/16'
            elif dec <= 3/8 + 1/32:
                dec = '3/8'
            elif dec <= 7/16 + 1/32:
                dec = '7/16'
            elif dec <= 1/2 + 1/32:
                dec = '1/2'
            elif dec <= 9/16 + 1/32:
                dec = '9/16'
            elif dec <= 5/8 + 1/32:
                dec = '5/8'
            elif dec <= 11/16 + 1/32:
                dec = '11/16'
            elif dec <= 3/4 + 1/32:
                dec = '3/4'
            elif dec <= 13/16 + 1/32:
                dec = '13/16'
            elif dec <= 7/8 + 1/32:
                dec = '7/8'
            elif dec <= 31/32:
                dec = '15/16'
            else:
                if whole:
                    return int(whole) + 1
                else:
                    return 1
                
            if whole:
                return f"{whole} {dec}"
            else:
                return dec
    except IndexError:
        print("invalid input. exiting...")
        sys.exit(0)

def frac_to_dec(num):
    # takes a number (possibly with a fraction) of type string and converts to an int or float
    # int (without decimal) or float (with decimal)
    feet = 0
    inches = 0
    decimal = 0

    def get_fraction(frac):
            numerator = float(frac.split('/')[0])
            denominator = float(frac.split('/')[1])

            return numerator / denominator

    if type(num) != str:
        num = str(num)
    
    try:
        num = num.split(' ')
        for index, value in enumerate(num):
            if "'" in value:
                feet = int(num[index][:-1])
            elif not '/' in value:
                if '"' in value:
                    inches = int(num[index][:-1])
                    continue
                inches = int(num[index])
            elif '/' in value:
                if '"' in value:
                    decimal = get_fraction(num[index][:-1])
                    continue
                decimal = get_fraction(num[index])
    except Exception as e:
        print(f'Error enumerating through num list in frac_to_dec: {e}')

    return (feet * 12) + inches + decimal


    ##### UNIT WEIGHTS in lbs/ft^3 #####
'''
steel = 490
aluminum = 165
concrete = 150
wood = 50
water = 62
sand and gravel = 120
copper = 560
oil = 58
'''

#-----------------------------------------------------------------------------------
#                   RADIAL MATH FUNCS
#-----------------------------------------------------------------------------------

def get_chord_len(arc, rad):
    cen_angle = arc / rad
    chord_len = (2 * rad) * math.sin(cen_angle / 2)

    return chord_len

def get_stretchout(dia):
    stretchout = dia * math.pi

    return stretchout

def get_run(bot, top):
    run = (bot - top) / 2

    return run

def get_hypotenuse(run, h):
    base = h**2 + run**2
    hypotenuse = math.sqrt(base)

    return hypotenuse

def get_angle(h, run):
    angle = math.atan(h/run)

    return angle

def get_radius(run, angle):
        radius = run / math.cos(angle)

        return radius

def get_slope_intercept():
    pass

#-----------------------------------------------------------------------------------
#                   FINDING MISSING SIDE FUNCS
#-----------------------------------------------------------------------------------

def get_pythagorean(hypotenuse=None, side=None, second=None):
    if hypotenuse is not None:
        third = hypotenuse**2 - second**2
        third = round(math.sqrt(third), 2)

        print(f'\nthird side is {third}')
        sys.exit(1)
    
    hypotenuse = side**2 + second**2
    hypotenuse = round(math.sqrt(hypotenuse), 2)

    print(f'\nhypotenuse is {hypotenuse}')
    sys.exit(1)

def SOH(angle=None, side=None, hypotenuse=None):
    if hypotenuse:
        side = math.sin(math.degrees(angle)) * hypotenuse

        print(f'the length of your side is {round(side, 2)}')
        sys.exit(1)
    elif not hypotenuse:
        hypotenuse = side / math.sin(angle)

        print(f'your hypotenuse is {round(hypotenuse, 2)}')
        sys.exit(1)
    else:
        print('error in SOH, else, exiting...')
        sys.exit(0)

def CAH(angle=None, side=None, hypotenuse=None):
    if hypotenuse:
        side = math.cos(math.degrees(angle)) * hypotenuse

        print(f'the length of your side is {round(side, 2)}')
        sys.exit(1)
    elif not hypotenuse:
        hypotenuse = side / math.cos(angle)

        print(f'your hypotenuse is {round(hypotenuse, 2)}')
        sys.exit(1)
    else:
        print("error in CAH, else, exiting...")
        sys.exit(0)

def TOA(angle, side=None, hypotenuse=None):
    print('Tangent not working. come back later or try using Sine or Cosine. exiting...')
    sys.exit(0)

def SOHCAHTOA(angle=None, side=None, hypotenuse=None):
    if hypotenuse is None:
        which_side_q = input("is your side [adj]acent to or [opp]osite of the angle? ").lower()
    else:
        which_side_q = input("is the side you're finding [adj]acent to or [opp]osite from your angle?").lower()

    if not angle:
        angle = float(input("degree of angle: "))
    angle = math.radians(angle)

    if 'opp' in which_side_q:
        SOH(angle=angle, side=side, hypotenuse=hypotenuse)
    elif 'adj' in which_side_q:
        CAH(angle=angle, side=side, hypotenuse=hypotenuse)
#    elif 'toa' in which_side_q:                        UNDER CONSTRUCTION (do we even need?)
#    TOA(angle, side=side, hypotenuse=hypotenuse)
    else:
        print('unknown input. exiting...')
        sys.exit(0)

#-----------------------------------------------------------------------------------
#                   FINDING MISSING ANGLE FUNCS
#-----------------------------------------------------------------------------------

def arc_SOH(hypotenuse=None, side=None, angle=None):
    angle = math.asin(side/hypotenuse)
    print(f"your angle is {round(math.degrees(angle), 3)}")

    sys.exit(1)

def arc_CAH(hypotenuse=None, side=None, angle=None):
    angle = math.acos(side/hypotenuse)
    print(f"your angle is {round(math.degrees(angle), 3)}")

    sys.exit(1)

def arc_TOA(adj=None, opp=None, angle=None):
    angle = math.atan(opp/adj)
    print(f"your angle is {round(math.degrees(angle), 3)}")

    sys.exit(1)

#-----------------------------------------------------------------------------------
#                   FINDING MISSING TRIANGLE MAIN
#-----------------------------------------------------------------------------------

def find_whats_missing():
    angle_or_side = input('angle or side? ').lower()
    if 'angle' in angle_or_side:
        find_missing_angle()
    elif 'side' in angle_or_side:
        find_missing_side()
    else:
        print("unknown input. exiting...")
        sys.exit(0)

def find_missing_side():
    num_sides = int(input('how many sides do you have? '))

    if num_sides == 2:
        hyp_q = input('is one of them the hypotenuse? ').lower()
        if 'y' in hyp_q:
            hypotenuse = float(input('length of hypotenuse: '))
            other = float(input('length of other side: '))
            get_pythagorean(hypotenuse, second=other)
        elif 'n' in hyp_q:
            side = float(input("length of first side: "))
            second = float(input("length of second side: "))
            get_pythagorean(side=side, second=second)
    elif num_sides == 0:
        print('you need at least one side to find a second side. exiting...')
        sys.exit(0)
    elif num_sides == 1:
        if 'y' in input('do you have at least one angle? ').lower():
            find_hypot_q = input("is the side you're finding the hypotenuse? ").lower()
            if 'y' in find_hypot_q:
                side = float(input("length of side: "))
                angle = float(input("degree of angle: "))
                SOHCAHTOA(angle=angle, side=side)
            elif 'n' in find_hypot_q:
                have_hyp_q = input("do you have the hypotenuse? ").lower()
                if 'y' in have_hyp_q:
                    hypotenuse = float(input('length of hypotenuse: '))
                    angle = math.radians(float(input("angle degree: ")))
                    SOHCAHTOA(angle=angle, hypotenuse=hypotenuse)
                elif 'n' in have_hyp_q:
                        side = float(input("length of side: "))
                        angle = float(input("angle degree: "))
                        SOHCAHTOA(angle=angle, side=side)
        else:
            print('you need at least one angle and one side. exiting...')
            sys.exit(0)
    else:
        print("invalid number of sides. exiting...")
        sys.exit(0)

def find_missing_angle():
    third_side_q = input("are you finding your third angle? ")
    if 'y' in third_side_q:
        angle = float(input("degree of second angle (not 90): "))
        print(f'your third angle is {round(90 - angle, 2)}')
        
        return

    num_sides = int(input("how many sides do you have? "))
    if num_sides == 2:
        # this without asking if one is hypotenuse for 3
        if 'y' in input("is one of them the hypotenuse? ").lower():
            hypotenuse = float(input("length of hypotenuse: "))
            other_side = input("is your other side [adj]acent to or [opp]osite from the angle? ").lower()
            side_len = float(input("length of said side: "))
            if 'adj' in other_side:
                arc_CAH(hypotenuse=hypotenuse, side=side_len)
            elif 'opp' in other_side:
                arc_SOH(hypotenuse=hypotenuse, side=side_len)
            else:
                print("unknown input in two angles, adjace or opposite. exiting...")
                sys.exit(0)
        else:
            adj = float(input("length of adjacent side (relative to known angle): "))
            opp = float(input("length of opposite side: "))
            arc_TOA(adj=adj, opp=opp)
    elif num_sides == 3:
        hypotenuse = float(input("length of hypotenuse: "))
        adj = float(input("length of side adjacent to angle: "))
        arc_CAH(side=adj, hypotenuse=hypotenuse)
    elif num_sides == 1:
        hyp_q = input("is your known side the hypotenuse? ")
        if 'y' in hyp_q:
            hypotenuse = float(input("length of hypotenuse: "))
            angle = float(input("degree of angle: "))
            which_side = input("which side are you wanting to find (relative to the angle)? [adj]acent or [opp]osite: ").lower()
            if 'adj' in which_side:
                arc_CAH(hypotenuse=hypotenuse, angle=angle)
            elif 'opp' in which_side:
                arc_SOH(hypotenuse=hypotenuse, angle=angle)
            else:
                print("unknown input. exiting...")
                sys.exit(0)
        elif 'n' in hyp_q:
            side_q = input("where is side relative to known angle? ([adj]acent or [opp]osite): ").lower()
            side = float(input("length of side: "))
            angle = float(input("degree of angle: "))

            if 'adj' in side_q:
                arc_CAH(side=side, angle=angle)
            elif 'opp' in side_q:
                arc_SOH(side=side, angle=angle)
            else:
                print("unknown input. exiting...")
                sys.exit(0)
    else:
        print("you need at least one side and an angle to find a second angle. exiting...")
        sys.exit(0)

#-----------------------------------------------------------------------------------
#                   RADIAL MATH MAIN
#-----------------------------------------------------------------------------------

def find_swing(dec=None, pitch=None):

    # find height of taper using pitch
    # gives negative pitch with args (td:4, bd:6, th:4)
    # ^^ add flow telling person to flip their cone around

    top_dia = float(input("top diameter: "))
    bot_dia = float(input("bot diameter: "))
    height = float(input("taper height: "))
    if pitch:
        print("pitch currently under construction. exiting...")
        sys.exit(0)
        '''
        pitch = float(input("pitch (in fraction): "))
        pitch = frac_to_dec(pitch)
        '''


    bot_stretchout = get_stretchout(bot_dia)
    bot_run = get_run(bot_dia, top_dia)
    bot_hyp = get_hypotenuse(bot_run, height)
    angle = get_angle(height, bot_run)
    top_run = top_dia / 2
    top_radius = get_radius(top_run, angle)
    bot_radius = top_radius + bot_hyp

    chord = get_chord_len(bot_stretchout, bot_radius)

    if dec:
        print(f"\nbot stretchout: {round(bot_stretchout, 2)}")
        print(f"top radius: {round(top_radius, 2)}")
        print(f"bot radius: {round(bot_radius, 2)} ({round(bot_hyp, 2)})")
        print(f"angle: {round(math.degrees(angle), 3)}")
        print(f"chord length: {round(chord, 2)}")

        return

    print(f"\nbot stretchout: {dec_to_frac(bot_stretchout)}")
    print(f"top radius: {dec_to_frac(top_radius)}")
    print(f"bot radius: {dec_to_frac(bot_radius)} ({dec_to_frac(bot_hyp)})")
    print(f"pitch: {round(math.degrees(angle), 3)}")
    print(f"chord length: {dec_to_frac(chord)}")
    if pitch:
        pass

    return

#-----------------------------------------------------------------------------------
#                   Parallel Line
#-----------------------------------------------------------------------------------

    #   takes three required args and one optional:
    #   in order -->  [diameter][elevation height][elevation angle][optional: # of sections]

    #   returns circumference, section widths, opposite elevation height

class ParallelLine:
    def __init__(self, args):
        self.args = args
        self.diameter = num_to_dec(args.parallel[0])
        self.el_height = num_to_dec(args.parallel[1])
        self.el_angle = args.parallel[2]
        if len(sys.argv) == 6:
            self.section = int(args.parallel[3])
        else:
            self.section = 12

    def get_stretchout(self):
        # get circumference
        return math.pi * self.diameter

    def get_sections(self):
        # circumference / # of sections
        return dec_to_frac(self.diameter / self.section)
    
    def get_elevation_height(self):
        return dec_to_frac(self.diameter / math.cos(self.el_angle))

    def run(self):
        circumference = self.get_stretchout(self.args.diameter)
        section_size = self.get_sections(circumference)
        elevation_height = self.get_elevation_height(self.args.angle, self.args.diameter)
        return circumference, section_size, elevation_height


#-----------------------------------------------------------------------------------
#                       MAIN
#-----------------------------------------------------------------------------------

def main():
    # option to add: if --decimal, output to decimal instead of fractional
    # possibly add option of verbosity
    # add try catch to everything
    # possibly port some function groups to classes
    
    # eventually create front end and host this on web, make for security project with \\
    # login credentials, potential vulnerability testing, honeypot type deal

    parser = argparse.ArgumentParser(
        prog="JATC_calc",
        description="poor mans calculator",
    )
    parser.add_argument('-a', '--angle', nargs='?', help='find angle')
    parser.add_argument('-s', '--side', nargs='?', help='find side')
    parser.add_argument('-r', '--radial', nargs='?', help='radial line layout')
    parser.add_argument('-c', '--convert', action='store_true', help='input to encrypt')
    parser.add_argument('-p', '--parallel', nargs='*', help='parallel line layout')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        _usage()
    elif args.angle:
        pass
    elif args.side:
        pass
    elif args.radial:
        pass
    elif args.parallel:
        # args: diamater, elevation height, elevation angle, (opt) # of sections

        if len(sys.argv) < 5:
            _usage(param='parallel')
        try:
            (sys.argv[2])
        except:
            pass
        parallel = ParallelLine(args)
        circum, section_size, elevation_height = parallel.run()
        print(f'')
        sys.exit(0)
    elif args.convert:
        pass
    else:
        _usage()


    if sys.argv[1] == '--find':
        if len(sys.argv) == 3:
            if sys.argv[2] == 'angle':
                find_missing_angle()
                sys.exit(1)

            if sys.argv[2] == 'side':
                find_missing_side()
                sys.exit(1)

        find_whats_missing()
    elif sys.argv[1] == '--radial':
        if len(sys.argv) > 2:
            # fix to allow for both dec and pitch
            if 'dec' in sys.argv[2]:
                find_swing(dec=True)
            if 'pitch' in sys.argv[2]:
                # add usage
                find_swing(pitch=True)
        find_swing()
    elif sys.argv[1] == '--convert':
        if len(sys.argv) == 3:
            frac = dec_to_frac(sys.argv[2])
            print(frac)
            sys.exit(1)
        dec = input("decimal to convert: ")
        frac = dec_to_frac(dec)
        print(frac)
        sys.exit(1)
    else:
        _usage()


if __name__ == "__main__":
    main()
