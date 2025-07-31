from src.robot.models.robot import Direction, Position, Robot


def test_initial_robot_position():
    """Test robot initializes with correct starting position and direction"""
    robot = Robot(position=(0, 0), direction=Direction.NORTH)
    assert robot.position == Position(x=0, y=0)
    assert robot.direction == Direction.NORTH


def test_robot_moves_forward_north():
    """Test robot moves forward when facing north"""
    robot = Robot(position=(0, 0), direction=Direction.NORTH)
    robot.move_forward()
    assert robot.position == Position(x=0, y=1)


def test_robot_moves_forward_south():
    """Test robot moves forward when facing south"""
    robot = Robot(position=(0, 1), direction=Direction.SOUTH)
    robot.move_forward()
    assert robot.position == Position(x=0, y=0)


def test_robot_moves_forward_east():
    """Test robot moves forward when facing east"""
    robot = Robot(position=(0, 0), direction=Direction.EAST)
    robot.move_forward()
    assert robot.position == Position(x=1, y=0)


def test_robot_moves_forward_west():
    """Test robot moves forward when facing west"""
    robot = Robot(position=(1, 0), direction=Direction.WEST)
    robot.move_forward()
    assert robot.position == Position(x=0, y=0)


def test_robot_rotates_left():
    """Test robot rotates left (counter-clockwise) correctly"""
    robot = Robot(position=(0, 0), direction=Direction.NORTH)
    robot.rotate_left()
    assert robot.direction == Direction.WEST

    robot.rotate_left()
    assert robot.direction == Direction.SOUTH

    robot.rotate_left()
    assert robot.direction == Direction.EAST

    robot.rotate_left()
    assert robot.direction == Direction.NORTH


def test_robot_rotates_right():
    """Test robot rotates right (clockwise) correctly"""
    robot = Robot(position=(0, 0), direction=Direction.NORTH)
    robot.rotate_right()
    assert robot.direction == Direction.EAST

    robot.rotate_right()
    assert robot.direction == Direction.SOUTH

    robot.rotate_right()
    assert robot.direction == Direction.WEST

    robot.rotate_right()
    assert robot.direction == Direction.NORTH


def test_robot_moves_backward():
    """Test robot moves backward in the direction it's facing"""
    # Facing north, moving backward goes south
    robot = Robot(position=(0, 0), direction=Direction.NORTH)
    robot.move_backward()
    assert robot.position == Position(x=0, y=-1)

    # Facing east, moving backward goes west
    robot = Robot(position=(0, 0), direction=Direction.EAST)
    robot.move_backward()
    assert robot.position == Position(x=-1, y=0)
