from gcodeparser import GcodeParser

if __name__ == '__main__':
    with open('3DBenchy.gcode', 'r') as f:
        gcode = f.read()
    parsed_gcode = GcodeParser(gcode)
    pass
