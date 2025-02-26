from redminelib import Redmine
from config import redmine_token


class RedmineConnector:
    def __init__(self, project='helpdesk'):
        self.url = 'http://rmlocal2.fb'
        self.project = project
        self.key = redmine_token
        self.redmine = Redmine(url=self.url, key=self.key)
        self.telegram_field_id = 1
        self.zakazchik_field_id = 2

    def create_issue(self, task_subject, task_description, tracker_id, telegram_id):
        """
        Функция создания задачи в редмайне

        :param tracker_id: ID трекера задачи (Ошибка, Улучшение, Поддержка)
        :param task_subject: Тема задачи
        :param task_description: Описание задачи
        :return: ID созданной задачи в Redmine
        """
        # Формирует custom field 'Заказчик'
        rm_user = self.get_user_by_id(str(telegram_id))
        if rm_user is not None:
            custom_fields = [{'id': self.zakazchik_field_id, 'value': rm_user.id}]
        else:
            custom_fields = []
        redmine_project = self.redmine.project.get(self.project)
        issue = self.redmine.issue.create(project_id=redmine_project.id, tracker_id=tracker_id, subject=task_subject,
                                          description=task_description, custom_fields=custom_fields)
        return issue.id

    def get_issue_status(self, issue_id):
        """
        Получение информации о задачи в редмайне по номеру (проект не важен)

        :param issue_id: Номер задачи в редмайне
        :return: Статус задачи str
        """
        issue = self.redmine.issue.get(issue_id, include=['children', 'journals', 'watchers'])
        return issue.status

    def get_issue(self, issue_id):
        """
        Получение информации о задачи в редмайне по номеру (проект не важен)

        :param issue_id: Номер задачи в редмайне
        :return: Статус задачи str
        """
        issue = self.redmine.issue.get(issue_id, include=['children', 'journals', 'watchers'])
        return issue

    def increase_issue_priority(self, issue_id):
        """
        Увеличение приоритета задачи

        :param issue_id: Номер задачи в редмайне str
        :return: None
        """
        issue = self.get_issue(issue_id)
        priority = issue.priority.id
        if priority < 5:
            self.redmine.issue.update(issue_id, priority_id=priority + 1)

    def decrease_issue_priority(self, issue_id):
        """
        Уменьшение приоритета задачи

        :param issue_id: Номер задачи в редмайне str
        :return: None
        """
        issue = self.get_issue(issue_id)
        priority = issue.priority.id
        if priority > 2:
            self.redmine.issue.update(issue_id, priority_id=priority - 1)

    def get_user_by_id(self, telegram_id):
        """
        Ищет в редмайне пользователя по Custom_field 'Telegram ID'

        :param telegram_id: Telegram id пользователя str
        :return: User object, or None
        """
        rm_users = self.redmine.user.filter(status=1)
        for user in rm_users:
            if user.custom_fields.get(self.telegram_field_id).value == telegram_id:
                return user
        return None



# tele = '779500420'
# rm = RedmineConnector()
# users = rm.get_user_by_id(tele)
# print(users)