from locust import HttpUser, task



class GUDLFTUser(HttpUser):
    # competition = loadCompetitions()[0]
    competition = {
        "name": "Fall festival",
        "date": "2024-10-22 13:30:00",
        "numberOfPlaces": "5",
    }
    # club = loadClubs()[0]
    club = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "15"}

    @task
    def access_index(self):
        self.client.get("/")

    @task
    def access_summary(self):
        self.client.post("/showSummary", data={"email": self.club["email"]})

    @task
    def book_competition(self):
        self.client.get(f"/book/{self.competition['name']}/{self.club['name']}")

    @task
    def purchase_places(self):
        self.client.post(
            "/purchasePlaces",
            data={
                "places": 1,
                "club": self.club["name"],
                "competition": self.competition["name"],
            },
        )

    @task
    def access_board(self):
        self.client.get(f"/board?club={self.club['name']}")

    @task
    def logout(self):
        self.client.get("/logout")
