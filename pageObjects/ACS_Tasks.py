import time
from selenium import common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from utilities.ReadAcsProperties import ReadConfig_ACS_Environment
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains


class AcsTasks:
    text_taskList = '//*[@id="upTasksRefresh"]'
    text_pendingTask_xpath = '//*[@id="tblTasksStatus"]/table/tbody/tr[1]/td[1]'
    text_sentTask_id_xpath = '//*[@id="tblTasksStatus"]/table/tbody/tr[2]/td[1]'
    text_completedTask_xpath = '//*[@id="tblTasksStatus"]/table/tbody/tr[3]/td[1]'
    text_rejectedTask_xpath = '//*[@id="tblTasksStatus"]/table/tbody/tr[4]/td[1]'
    text_failedTask_xpath = '//*[@id="tblTasksStatus"]/table/tbody/tr[5]/td[1]'

    text_pendingTask_id = 'lblPendingCount'
    text_sentTask_id_id = 'lblSentCount'
    text_completedTask_id = 'lblCompletedCount'
    text_rejectedTask_id = 'lblRejectedCount'
    text_failedTask_id = 'lblFailedCount'

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def scrollToTask(self):
        element = self.driver.find_element(By.XPATH, self.text_taskList)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()

    def PendingTask(self):
        PendingTask = self.driver.find_element(By.ID, self.text_pendingTask_id).text
        print('Number of Pending Task : ' + str(PendingTask))
        return PendingTask

    def SentTask(self):
        SentTask = self.driver.find_element(By.ID, self.text_sentTask_id_id).text
        print('Number of Sent Task : ' + str(SentTask))
        return SentTask

    def CompletedTask(self):
        CompletedTask = self.driver.find_element(By.ID, self.text_completedTask_id).text
        print('Number of Completed Task : ' + str(CompletedTask))
        return CompletedTask

    def RejectedTask(self):
        RejectedTask = self.driver.find_element(By.ID, self.text_rejectedTask_id).text
        print('Number of Rejected Task : ' + str(RejectedTask))
        return RejectedTask

    def FailedTask(self):
        FailedTask = self.driver.find_element(By.ID, self.text_failedTask_id).text
        print('Number of Failed Task : ' + str(FailedTask))
        return FailedTask
