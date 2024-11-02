from fastapi.testclient import TestClient
from fastapi import status
import asyncio
import sys


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class FrogHelper:
    prefix = "/frogs/"
    frog_id_for_test = 1_637
    frog_id_for_test_does_not_exist = 98_393_892

    @staticmethod
    def create_frog_payload(
        frog_id: int | None = None,
        name: str = "David",
        age: int = 2,
        description: str | None = None,
    ) -> dict[str, str | int]:
        data = {
            "name": name,
            "age": age,
            "description": description,
        }
        if frog_id:
            data["id"] = frog_id

        return data


class TestPostMethods:
    __prefix_create = FrogHelper.prefix + "create/"

    @staticmethod
    def __create_frog_payload(
        frog_id: int | None = None,
        name: str = "David",
        age: int = 2,
        description: str | None = None,
    ) -> dict[str, str | int]:
        return FrogHelper.create_frog_payload(
            frog_id=frog_id,
            name=name,
            age=age,
            description=description,
        )

    def test_create_frog(self, client: TestClient) -> None:
        payload = self.__create_frog_payload(
            frog_id=FrogHelper.frog_id_for_test
        )
        response = client.post(self.__prefix_create, json=payload)
        assert response.status_code == status.HTTP_201_CREATED

        assert response.json() == payload

    def test_create_frog_status_code_default_conflict(
        self, client: TestClient
    ) -> None:
        payload = self.__create_frog_payload(
            frog_id=FrogHelper.frog_id_for_test
        )
        response = client.post(self.__prefix_create, json=payload)
        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json()["detail"] == "frog already exists"

    def test_create_frog_without_id(self, client: TestClient) -> None:
        payload = self.__create_frog_payload()
        response = client.post(self.__prefix_create, json=payload)
        assert response.status_code == status.HTTP_201_CREATED


class TestGetMethods:
    __prefix_all = FrogHelper.prefix
    __prefix_by_id = __prefix_all + "{frog_id}/"

    def __get_by_id_url(self, frog_id: int = 1) -> str:
        return self.__prefix_by_id.replace("{frog_id}", str(frog_id))

    def test_get_all_frogs_status_code(self, client: TestClient) -> None:
        response = client.get(self.__prefix_all)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_id_status_code_default(self, client: TestClient) -> None:
        url = self.__get_by_id_url(FrogHelper.frog_id_for_test)

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_get_by_id_status_code_not_found(self, client: TestClient) -> None:
        url = self.__get_by_id_url(FrogHelper.frog_id_for_test_does_not_exist)

        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_by_id_response(self, client: TestClient) -> None:
        frog_data = FrogHelper.create_frog_payload(
            frog_id=FrogHelper.frog_id_for_test
        )
        url = self.__get_by_id_url(FrogHelper.frog_id_for_test)

        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == frog_data


class TestUpdateMethods:
    __prefix_update = FrogHelper.prefix + "update/"

    def test_update_frog_code_status_default(self, client: TestClient) -> None:
        frog_data = FrogHelper.create_frog_payload(
            frog_id=FrogHelper.frog_id_for_test,
            name="Oleg",
            description="updated",
        )

        response = client.put(self.__prefix_update, json=frog_data)
        assert response.status_code == status.HTTP_200_OK

    def test_update_frog_status_response_value(
        self, client: TestClient
    ) -> None:
        frog_data = FrogHelper.create_frog_payload(
            frog_id=FrogHelper.frog_id_for_test,
            name="Denis",
            age=4,
            description="updated",
        )

        response = client.put(self.__prefix_update, json=frog_data)
        assert response.json()["message"] == "frog updated"

    def test_update_frog_code_status_404(self):
        pass


class TestDeleteMethods:
    __prefix_delete = FrogHelper.prefix + "delete/{frog_id}/"

    def __get_delete_url(self, frog_id: int = 1) -> str:
        return self.__prefix_delete.replace("{frog_id}", str(frog_id))

    def test_delete_frog_by_id(self, client: TestClient) -> None:
        url = self.__get_delete_url(FrogHelper.frog_id_for_test)
        response = client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "frog has been removed"

    def test_delete_frog_by_does_not_exist_id(
        self, client: TestClient
    ) -> None:
        url = self.__get_delete_url(FrogHelper.frog_id_for_test_does_not_exist)
        response = client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "frog has been removed"
