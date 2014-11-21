from pixie.vm.effects.effects import Object, Type
import pixie.vm.effects.effects as effects
from pixie.vm.primitives import nil
from rpython.rlib.objectmodel import specialize


class Keyword(Object):
    _type = Type(u"pixie.stdlib.Keyword")
    __immutable_fields__ = ["_hash", "_str"]
    def __init__(self, name):
        self._str = name
        self._w_name = None
        self._w_ns = None
        self._hash = 0

    def type(self):
        return Keyword._type

    def init_names(self):
        if self._w_name is None:
            s = self._str.split(u"/")
            if len(s) == 2:
                self._w_ns = rt.wrap(s[0])
                self._w_name = rt.wrap(s[1])
            elif len(s) == 1:
                self._w_name = rt.wrap(s[0])
                self._w_ns = nil
            else:
                self._w_ns = rt.wrap(s[0])
                self._w_name = rt.wrap(u"/".join(s[1:]))


    def __repr__(self):
        return ":" + str(self._str)

    def __str__(self):
        return self.__repr__()


class KeywordCache(object):
    def __init__(self):
        self._cache = {}

    def intern(self, nm):
        kw = self._cache.get(nm, None)

        if kw is None:
            kw = Keyword(nm)
            self._cache[nm] = kw

        return kw

_kw_cache = KeywordCache()

@specialize.argtype(0)
def keyword(nm):
    return _kw_cache.intern(nm if isinstance(nm, unicode) else unicode(nm))

effects.KW_K = keyword("k")

#
# @extend(proto._name, Keyword)
# def _name(self):
#     assert isinstance(self, Keyword)
#     self.init_names()
#     return self._w_name
#
# @extend(proto._namespace, Keyword)
# def _namespace(self):
#     assert isinstance(self, Keyword)
#     self.init_names()
#     return self._w_ns
#
# @extend(proto._hash, Keyword)
# def _hash(self):
#     assert isinstance(self, Keyword)
#     if self._hash == 0:
#         self._hash = util.hash_unencoded_chars(self._str)
#     return rt.wrap(intmask(self._hash))
#
# @as_var("keyword")
# def _keyword(s):
#     affirm(isinstance(s, String), u"Symbol name must be a string")
#     return keyword(s._str)