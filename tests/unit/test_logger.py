from app.infra.logger import get_logger, logger


def test_base_logger_exists():
    assert logger.name == "fastapi_template"
    assert logger.handlers, "Logger should have at least one handler"


def test_get_logger_child():
    child = get_logger("app.modules.health.service")
    assert child.name == "fastapi_template.app.modules.health.service"
    assert child.handlers == [], "Child logger should not add its own handlers"
    assert child.propagate is True
