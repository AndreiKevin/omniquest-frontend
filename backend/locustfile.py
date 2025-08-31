from locust import HttpUser, task, between
from random import choice, randint


CATEGORIES = [
    "Baking", "Beverages", "Bread", "Breakfast Foods", "Candy",
    "Canned Goods", "Condiments", "Dairy", "Deli", "Frozen Foods",
    "Meat", "Produce", "Seafood", "Snacks",
]


class ProductUser(HttpUser):
    wait_time = between(0.2, 1.0)

    @task(5)
    def page_1_default(self):
        self.client.get("/products?page=1&page_size=24")

    @task(3)
    def paginate_next(self):
        page = randint(2, 10)
        self.client.get(f"/products?page={page}&page_size=24")

    @task(2)
    def filter_multi_categories(self):
        cats = ",".join({choice(CATEGORIES) for _ in range(2)})
        self.client.get(f"/products?page=1&page_size=24&categories={cats}")

    @task(2)
    def sort_price_asc(self):
        self.client.get("/products?page=1&page_size=24&sort=price_asc")

    @task(2)
    def sort_price_desc(self):
        self.client.get("/products?page=1&page_size=24&sort=price_desc")

    @task(1)
    def categories_and_sort(self):
        cats = ",".join({choice(CATEGORIES) for _ in range(2)})
        self.client.get(f"/products?page=1&page_size=24&categories={cats}&sort=price_desc")



