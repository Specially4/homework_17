import logging

new_logger = logging.getLogger()

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("basic.log")
formatter_new = logging.Formatter('''
Message type:       %(levelname)s
Location:           %(pathname)s:%(lineno)d
Time:               %(asctime)s
Message:
%(message)s
''')
console_handler.setFormatter(formatter_new)
file_handler.setFormatter(formatter_new)
new_logger.addHandler(console_handler)
new_logger.addHandler(file_handler)