class A:
    def __init__(self, **kwa):
        a = kwa.pop('a')
        print("A kwa: %s" % kwa)

class B(A):
    def __init__(self, **kwa):
        b = kwa.pop('b')
        print("B kwa: %s" % kwa)
        super(B, self).__init__(**kwa)

class C(B):
    def __init__(self, **kwa):
        c = kwa.pop('c')
        print("C kwa: %s" % kwa)
        super(C, self).__init__(**kwa)


C(a='aaa', b='bbb', c='ccc')