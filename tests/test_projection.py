from src.utils.projection import world_to_screen

IDENTITY = [
    1.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 1.0,
]


def test_center_world_maps_to_screen_center():
    pt = world_to_screen(IDENTITY, (0.0, 0.0, 1.0), (1920, 1080))
    assert pt == (960, 540)


def test_behind_camera_returns_none():
    assert world_to_screen(IDENTITY, (0.0, 0.0, -1.0), (1920, 1080)) is None