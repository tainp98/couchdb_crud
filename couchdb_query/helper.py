import inspect
from datetime import date, datetime
def func_info():
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  file_name = 'File "' + info.filename + '"'
  func_name = 'in ' + info.function
  line = 'line ' + str(info.lineno)
  return file_name, func_name, line

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))