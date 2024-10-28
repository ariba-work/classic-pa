from util import constants
from util.constants import DependencyTypes


def _get_move_label(move):
    if not move[0] or not move[1]:  # silent transition
        return "\u03C4"  # tau

    if move[0] != constants.SKIP:  # log move
        return move[0]

    return move[1]  # model move


def _get_move_color(move):
    return _get_color_by_type(_get_type(move))


def _get_color_by_type(dep_type: str):
    if dep_type == DependencyTypes.MODEL.value:
        return 'blue'
    elif dep_type == DependencyTypes.LOG.value:
        return 'orange'
    elif dep_type == DependencyTypes.SYNCHRONOUS.value:
        return 'green'
    else:
        return 'gray'


def _get_move_shape(move):
    dep_type = _get_type(move)
    if dep_type == DependencyTypes.LOG.value:
        return 'triangle'
    elif dep_type == DependencyTypes.MODEL.value:
        return 'box'
    else:
        return 'house'


def _get_type(move: tuple[str]):
    if move[0] != constants.SKIP and move[1] == constants.SKIP:
        return DependencyTypes.LOG.value

    if move[0] != constants.SKIP and move[1] != constants.SKIP:
        return DependencyTypes.SYNCHRONOUS.value

    return DependencyTypes.MODEL.value
