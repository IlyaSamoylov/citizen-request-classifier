class BaseAppException(Exception):
	def __init__(self, detail: str = "Собственная ошибка приложения"):
		self.detail = detail
		super().__init__(detail)

class SeedCategoryException(BaseAppException):
	def __init__(self, detail: str = "Ошибка справочника"):
		self.detail = detail
		super().__init__(detail)