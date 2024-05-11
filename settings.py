try:
    from settings_prod import *
except ImportError:
    try:
        from settings_dev import *
    except ImportError:
        raise Exception("Config file not found.")

# 记录器级别
if ENABLE_ACCESS_LOG:
    log_acc_level = 10
else:
    log_acc_level = 100

if ENABLE_AUDIT_LOG:
    log_adt_level = 10
else:
    log_adt_level = 100

if ENABLE_ERROR_LOG:
    log_err_level = 10
else:
    log_err_level = 100
# 日志文件处理器级别
if ENABLE_ACCESS_LOG_FILE:
    log_acc_level_file = 10
else:
    log_acc_level_file = 100

if ENABLE_AUDIT_LOG_FILE:
    log_adt_level_file = 10
else:
    log_adt_level_file = 100

if ENABLE_ERROR_LOG_FILE:
    log_err_level_file = 10
else:
    log_err_level_file = 100
# 日志流处理器级别
if ENABLE_ACCESS_LOG_CONSOLE:
    log_acc_level_console = 10
else:
    log_acc_level_console = 100

if ENABLE_AUDIT_LOG_CONSOLE:
    log_adt_level_console = 10
else:
    log_adt_level_console = 100

if ENABLE_ERROR_LOG_CONSOLE:
    log_err_level_console = 10
else:
    log_err_level_console = 100
