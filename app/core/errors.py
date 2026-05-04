class BaseAppException(Exception):
	def __init__(self, detail: str = "Собственная ошибка приложения"):
		self.detail = detail
		super().__init__(detail)

class SeedCategoryException(BaseAppException):
	def __init__(self, detail: str = "Ошибка справочника"):
		self.detail = detail
		super().__init__(detail)

class RequestNotFoundError(BaseAppException):
	def __init__(self, request_id: int):
		self.detail = f"Запрос с id = {request_id} не найден"
		super().__init__(self.detail)

class ClarificationNotFoundError(BaseAppException):
	def __init__(self, request_id: int):
		self.detail = f"Пояснение для запроса id = {request_id} не найдено"
		super().__init__(self.detail)

class ClarificationAlreadyAnsweredError(BaseAppException):
	def __init__(self, clarification_id: int):
		self.detail = f"Пояснение id = {clarification_id} уже получило ответ"
		super().__init__(self.detail)

class ClassificationFailedError(BaseAppException):
	def __init__(self, request_id: int):
		self.detail = f"Не вышло классифицировать запрос {request_id}"
		super().__init__(self.detail)

class PersistenceError(BaseAppException):
	def __init__(self, detail: str = "Ошибка при попытке сохранить"):
		self.detail = detail
		super().__init__(detail)
