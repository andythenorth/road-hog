class BasePlatform(object):
    """
    Vehicles can optionally use a base platform.
    This can be e.g.
    - a complete locomotive, wagon, semi-tractor etc
    - a chassis and cab to which the body is composited
    """
    def __init__(self):
        print("__init__")

