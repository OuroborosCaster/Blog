from settings import *
import logging, datetime
import concurrent.futures


class AsyncHandler(logging.Handler):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self.setLevel(handler.level)

    def emit(self, record):
        self.executor.submit(self.handler.emit, record)

    def setFormatter(self, fmt):
        self.handler.setFormatter(fmt)

def lineNum(e):
    import traceback
    return traceback.extract_tb(e.__traceback__)[-1][1]


# 访问日志
log_acc = logging.getLogger('访问')
log_acc.setLevel(log_acc_level)

acc_fmt = logging.Formatter(
    f'%(asctime)s.%(msecs)03d {datetime.datetime.now().astimezone().strftime('%z')} - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

acc_sh = AsyncHandler(logging.StreamHandler())
acc_sh.setLevel(log_acc_level_console)
acc_sh.setFormatter(acc_fmt)
log_acc.addHandler(acc_sh)

acc_fh = AsyncHandler(logging.FileHandler('./logs/access.log', encoding='utf-8'))
acc_fh.setLevel(log_acc_level_file)
acc_fh.setFormatter(acc_fmt)
log_acc.addHandler(acc_fh)

# 审计日志
log_adt = logging.getLogger('审计')
log_adt.setLevel(log_adt_level)

adt_fmt = logging.Formatter(
    f'%(asctime)s.%(msecs)03d {datetime.datetime.now().astimezone().strftime('%z')} - %(name)s - %(filename)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

adt_sh = AsyncHandler(logging.StreamHandler())
adt_sh.setLevel(log_adt_level_console)
adt_sh.setFormatter(adt_fmt)
log_adt.addHandler(adt_sh)

adt_fh = AsyncHandler(logging.FileHandler('./logs/audit.log', encoding='utf-8'))
adt_fh.setLevel(log_adt_level_file)
adt_fh.setFormatter(adt_fmt)
log_adt.addHandler(adt_fh)

# 错误日志
log_err = logging.getLogger('错误')
log_err.setLevel(log_err_level)

err_fmt = logging.Formatter(
    f'\n%(asctime)s.%(msecs)03d {datetime.datetime.now().astimezone().strftime('%z')} - %(name)s - %(filename)s - %(lineno)d - %(funcName)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

err_sh = AsyncHandler(logging.StreamHandler())
err_sh.setLevel(log_err_level_console)
err_sh.setFormatter(err_fmt)
log_err.addHandler(err_sh)

err_fh = AsyncHandler(logging.FileHandler('./logs/error.log', encoding='utf-8'))
err_fh.setLevel(log_err_level_file)
err_fh.setFormatter(err_fmt)
log_err.addHandler(err_fh)
