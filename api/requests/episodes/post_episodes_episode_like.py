# # api/requests/episodes/post_like_episode.py
# from api.endpoints import Endpoints
# from utils.allure_curl import attach_curl, attach_response_details
# import allure
#
#
# @allure.step("Like episode: {episode_id}")
# def post_like_episode(api_client, app_config, token, episode_id: str):
#     """
#     Like episode by ID.
#
#     Args:
#         api_client: APIClient instance
#         app_config: App configuration dict
#         token: Authorization token
#         episode_id: Episode ID to like
#     """
#     api_client.set_token(token)
#     response = api_client.post(
#         Endpoints.POST_EPISODES_EPISODE_LIKE,
#         headers=app_config["headers"],
#         url_params={"episode": episode_id}
#     )
#     attach_curl(response, f"curl: POST /episodes/{episode_id}/like")
#     attach_response_details(response)
#     return response
#
#
# @allure.step("Unlike episode: {episode_id}")
# def delete_like_episode(api_client, app_config, token, episode_id: str):
#     """Remove like from episode"""
#     api_client.set_token(token)
#     response = api_client.delete(
#         Endpoints.DELETE_EPISODES_EPISODE_LIKE,
#         headers=app_config["headers"],
#         url_params={"episode": episode_id}
#     )
#     attach_curl(response, f"curl: DELETE /episodes/{episode_id}/like")
#     attach_response_details(response)
#     return response
