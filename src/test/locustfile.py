from locust import HttpUser, task, between

class WebsiteTestUser(HttpUser):
    wait_time = between(0.5, 1)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass

    @task(1)
    def post_message(self):
        self.client.post(
            "http://localhost:8932/process-message",
            json={"message_text": "load test", "user_alias": "load test"})
