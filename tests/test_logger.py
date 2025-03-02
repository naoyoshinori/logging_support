import logging
import os

from logging_support import ISO8601_Formatter, initialize_simple_logger


def test_iso8601_formatter():
    formatter = ISO8601_Formatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    time_str = formatter.formatTime(record)
    # ISO-8601形式かを簡易チェック
    assert "T" in time_str and "+" in time_str, "Should be ISO-8601 format"


def test_initialize_simple_logger(tmp_path):
    log_dir = str(tmp_path / "logs")
    logger = initialize_simple_logger(
        name="test_logger",
        log_dir=log_dir,
        level=logging.DEBUG,
        stream_handler_level=logging.INFO,
        file_handler_level=logging.WARNING,
    )

    # ログファイルが作成されているか確認
    log_file = os.path.join(log_dir, "test_logger.log")
    assert os.path.exists(log_file)

    # ログ出力のテスト
    logger.debug("Debug message")  # 出力されない
    logger.info("Info message")  # ストリームのみ
    logger.warning("Warning message")  # ストリームとファイル

    with open(log_file, "r") as f:
        content = f.read()
        assert "Warning message" in content
        assert "Info message" not in content
