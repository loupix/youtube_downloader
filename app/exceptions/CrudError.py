import logging

class CrudError(Exception):

	code = 500
	message = ""
	className = ""
	functionName = ""

	def __init__(self, className = "", functionName = "", message="", code=None):
		self.message=message
		self.className=className
		self.functionName=functionName
		super().__init__(self.message)

		if code is not None: self.code=code
		logger = logging.getLogger("db")
		logger.critical('%s - %s : %s' % (className, code, message))

	def __str__(self):
		return 'CrudError in %s %s : %s - %s' % (self.className, self.functionName, self.code, self.message)

