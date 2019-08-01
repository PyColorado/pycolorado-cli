import os

from requests import Session

from common.exceptions import APIException, ConfigurationError


class BufferException(APIException):
    pass


class Buffer(Session):
    def __init__(self):
        super().__init__()

        buffer_access_token = os.getenv("BUFFER_ACCESS_TOKEN")

        if not buffer_access_token:
            raise ConfigurationError(
                "BUFFER_ACCESS_TOKEN must be specified in your environment or dotenv file for this operation."
            )

        self.params = dict(access_token=buffer_access_token)

    @property
    def base_url(self):
        return "https://api.bufferapp.com/1"

    def profiles(self):
        response = self.get(f"{self.base_url}/profiles.json")

        if response.ok:
            return response.json()
        else:
            raise BufferException(
                "Invalid response on profiles endpoint", api_response=response
            )

    def twitter(self):
        return next(filter(lambda x: x["service"] == "twitter", self.profiles()))

    def create_post(self, profiles, text, photo_url, scheduled_at):

        response = self.post(
            f"{self.base_url}/updates/create.json",
            data={
                "profile_ids[]": map(lambda x: x["id"], profiles),
                "text": text,
                "media[photo]": photo_url,
                "media[thumbnail]": photo_url,
                "scheduled_at": scheduled_at.isoformat(),
            },
        )

        if response.ok:
            return response.json()
        else:
            raise BufferException(
                "Invalid response on updates endpoint", api_response=response
            )
