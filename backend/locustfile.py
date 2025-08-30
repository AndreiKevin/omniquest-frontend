from locust import HttpUser, task, between


class ProductUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def browse_products(self):
        self.client.get("/products?page=1&page_size=24")

    @task(1)
    def filter_and_sort(self):
        self.client.get("/products?page=1&page_size=24&category=Frozen%20Foods&sort=price_desc")


