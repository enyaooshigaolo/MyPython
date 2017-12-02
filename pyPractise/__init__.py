from pip._vendor.distlib.compat import raw_input
name = raw_input('what is you name?')
if name.endswith('tank'):
    print('hello tank')
elif name.endswith('zhangsan'):
    print('hello zhangsan')
else:
    print('hello stanger')