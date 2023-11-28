import psutil
import pytest

from selenium_scraper import Scraper


def test_scraper_init_del():
    """Check parser instance startup and shutdown."""
    scraper = Scraper.chrome(headless=True)
    process = scraper.driver.service.process.pid
    del scraper
    with pytest.raises(psutil.NoSuchProcess):
        psutil.Process(process)


def test_del_scraper_process_not_running(monkeypatch):
    """Check that the exception does not occur if the process is already killed."""
    monkeypatch.setattr(psutil.Process, "is_running", lambda _: False)
    scraper = Scraper.chrome(headless=True)
    del scraper


def test_del_scraper_process_running_no_children(monkeypatch):
    """Check parser instance shutdown with no children processes."""
    monkeypatch.setattr(psutil.Process, "is_running", lambda _: True)
    monkeypatch.setattr(psutil.Process, "children", lambda *_args, **_kwargs: [])

    scraper = Scraper.chrome(headless=True)
    process = scraper.driver.service.process.pid
    del scraper

    with pytest.raises(psutil.NoSuchProcess):
        psutil.Process(process)


def test_del_scraper_process_running_children(monkeypatch):
    """Check parser instance shutdown with `n_processes` children processes."""
    n_processes = 2

    def mock_kill(*_args, **_kwargs):
        nonlocal n_processes
        n_processes -= 1

    monkeypatch.setattr(psutil.Process, "is_running", lambda _: True)
    monkeypatch.setattr(psutil.Process, "children", lambda *_args, **_kwargs: [psutil.Process()] * n_processes)
    monkeypatch.setattr(psutil.Process, "kill", mock_kill)

    scraper = Scraper.chrome(headless=True)
    process = scraper.driver.service.process.pid
    del scraper

    with pytest.raises(psutil.NoSuchProcess):
        psutil.Process(process)
    # 2 children + 1 self._driver_process.kill()
    assert n_processes + 1 == 0
