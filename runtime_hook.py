import builtins

# 禁用 print 函数
builtins.print = lambda *args, **kwargs: None