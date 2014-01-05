#Readers Mapping Documents

----------

**This is a work in progress documentation!!!!!!!!!!!**

----------


The ReadersMappingDocuments (Rmdocs) is a Framework which try to make easy adding new files parsers. 
In it you can find two package: *models and *parsers. 
In the first you can add the classes which represent the file read. This classes will be called Doc (or RmDoc).
In the second you can add the parsers. The parses are python modules which must contain a method called parse defined as follows:

	def parse(file, *args, **kwargs):

This is the method that performs the file parsing and it must return a data object that can be read and processed by the constructor of the correspondent model.

In the RmDoc module it will be a single method which glow up all together.
