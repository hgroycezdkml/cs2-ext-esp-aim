from src.core.config_loader import _Raw


def test_defaults_are_sane():
    cfg = _Raw()
    assert cfg.esp.enabled is True
    assert cfg.aim.fov == 3.0
    assert cfg.overlay.click_through is True