#Rmdoc

----------

**This is a work in progress documentation!!!!!!!!!!!**

----------


The rmdocs are simply classes. These classes can implement or not an interface called IRmDoc that provides some capability to integrate the classes into the library

	class User(IRmDoc):
        class Address(object):
            class Phone():
                
                def __init__(self):
                    self.prefix = '081'
                    self.number = '123456'
                    
            def __init__(self, i):
                self.street = "penny lane n. " + str(i)+" "
                self.cod = "040404"
                self.phone = self.Phone()
        
        def init_reader(self, path, reader_args):
            pass
        
        def build_rmdoc(self, rmdoc_args):
            pass
        
        def init(self):
            self.__setattr__("name", "Monkey D.")
            self.__setattr__("surname", "Rufy" )
            self.__setattr__("address", self.Address(-1))
            addresses = []
            for i in range(0,10):
                addresses.append(self.Address(i))
            self.__setattr__("addresses", addresses) 

Here we can use a class `User` that represents an user with name, surname, addresses. Each `Address` has street, code and phone, each `Phone` has prefix and number.

*NB: We have hardcoded the attributes value but normally they are retrieved from external file source using * `init_reader` *and* `build_rmdoc`