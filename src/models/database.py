from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class RobotState(Base):
    """Tracks the current state of the robot"""

    __tablename__ = "robot_state"

    id = Column(Integer, primary_key=True, index=True)
    position_x = Column(Integer, default=0)
    position_y = Column(Integer, default=0)
    direction = Column(String(10), default="NORTH")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class CommandHistory(Base):
    """Tracks all commands sent to the robot"""

    __tablename__ = "command_history"

    id = Column(Integer, primary_key=True, index=True)
    command = Column(Text, nullable=False)
    position_x = Column(Integer)
    position_y = Column(Integer)
    direction = Column(String(10))
    obstacle_detected = Column(Boolean, default=False)
    stopped_at = Column(Integer, nullable=True)
    executed_at = Column(DateTime, default=datetime.utcnow)


class Obstacle(Base):
    """Tracks obstacles on the Moon surface"""

    __tablename__ = "obstacles"

    id = Column(Integer, primary_key=True, index=True)
    position_x = Column(Integer, nullable=False)
    position_y = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        # Ensure unique positions
        UniqueConstraint("position_x", "position_y", name="uq_obstacle_position"),
    )
