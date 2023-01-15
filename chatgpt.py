config = {
        "Authorization": "<Your Bearer Token Here>", # This is optional
        "session_token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..lrA1o7sEdl4NoeY_.b5dpUZhL3-uNTpoAFRbC_h5OiHQU7oKgH_MjdxDibuTPhjV2lKl7865dZqERK1jL6oaBepUS0QHJhjJTIiyUe9WcKEIM0M5h_brp7Us89nRWhk2kX62UHhoFgGD4iyvkrYfQUcSFSP0kBwQLifebpQyZRR7Q9gA6kzmm-C-0PMlhU7vvdbBO1VAHUNGGHNwhwPvLwG28j89V2193xihxJNHajpbxHeH8QE8ZBUBHfaEak06oDCp9n8CQsApLaIV5gbj_LlmzN5mGpQ150t8gf7QFu1L0WxcyEr1fj_DJdx4TUZ8KiRx8NmwpzVfQ7yGFaVzYxJ772MzmnzTMp-SnGbwoeLCBwLOVrVKpWqBTe7Vs2HTcVsxVMzvLrk32tg6jrTG41mn8jXnSauB5xWEY6qBL7xW_pkLJwquajNl-8dgjVbYG7tHWhyJHvDXRcXGVv76er-anIMWpEVqrzVcv23AVqOHoN8pbMLhuSSzo5U9D5X4PbUg213hGGR4DvpSAli6SeosQiPIgHV4p6vJVO4YSDT9YmcKnmzJjxX21bx4AYGcEO2ZnQf4XIt_KL4sxkTBgON6wAGjdYEzwlY83mANJIuJeB5jZ8njsP8MbtcuWrwZ0tR-q2Gjqiw_WFqGRi5eyX2o6arnjLcTCXFqCXnAHpS_GT2uEfDff4rtoMdnQp0ExCx7ZPJmOadem6x6nLW2K7QQJlupw3lD6EnOzHOh4NAA3UBJmKmcKvX53AjY6PplxbbJ3Mw_TEM-bU_PEkm-V9c0Ei7Phc7qxZxuUz7e5DeglhpWUFntehONp0h6T_fEiz2F6qM8go_myZHgNyxaObpQSL8Odj_a3VN2OLZ7MSMdHpmLvOupXQTbHfH6_aqyADorD2wQf2SnuGMmoAN4JfE8cdZEmtuBFDqqG7DV4vz1-L_5UuMhCgQFiz12GmA6nA6xRLnP-LqQKEIclRgowNjWHL_Gc1YJA14KdExvXpOCxfG5-EMmyjYBYJw9thmSMKodGfsrYAcPcllZsTqXGxPuZRhA-w8-6Qw8SHIqgUowfudZb25L8HoWtigVU_HhL242xmtAahJ4_aRCvWEzY-LeJXZLcVK2LuZ02zPRsnZfES7vWpNw070mWUPtAtmJO04dMsc3nTqBP-wP9f3bH5f--DFGD8W28xVJ2rQKtzOvNsVYvXcqrrVvTs7Be7t8SjOgF0XlqObQmi7RyAYeYM80XAqhqMlWQV72I8XIE0-m5CMcA7eU9avMMvNepA83EpXWCyZkTrQma_xBSb9G810Akh0noTy-KW5DCs0xYXBMQ0SWxMPByQGjLHdcSdsz5FdCJfQewj_2Nww8CbpH_WgqJJgyeP3_D7mBsHvVMEjkLdfHYmztl6JovBWCRodqPnOzj4DZeZP_ndBn_absHnMVRaN1LKLp5IyQ2YLQDe6r1578YLtDjwDElpscK24-3MUo4x0cmwEymmaeFEK6FvXb0OmdNGdcM9mJ6GIi9PX5Oyo7hDOOeOJU_cCZeoZXv_H0TJ6VoEFx0jyfgVlth8TICJE58BZuGnX-5z3vyAln-ZpvpdllJP-l2zhNySUxobZizGI6Ns0uF78v4t1FTcNQGKdWIwFm_vjHIpyBCCZHasr8RTAviHT-NiTKPEDuPuPyz8Wtxnv3etTBmpFnRulkjV2-gyJpZXmbMMk2IycrqEWD1KhutBLlJMC1QbS1dWVN7hCPNv9gfQVOvo42DyRCsagOlJCVkCQF8d2Q43eCzWbAs0drmCnnOlVnnRzNSAv7eNxn5SlmzdbQXJUBxzthRSwbLbJ3blHNOgKF-WFpZCoZwfdiBKsYfnqcSTfXxAMR8ihBplaw2kFDKWhBggjFSQQq-oXqkVLN4zq7-XOWzkrxMM4tMit1y27S16RFWDOlNA4hnnIspMkzIBYBQWk6y3EQbtX-pQPfpfO4OrZrAGTibecUX3SVVzLhyrAdP3DsIaEER6JI1KEr1zcrTkNDpBH0XmB9mCvoFHhfhrSmQDuewdY2UVlPD96hIdxluy5bAjSNZecxFrrTEyIxQ4VIbeQEAK0nBwD3v00mPt-J2TgHS-xvvt56YvAU8k21b3lTlYC5rhDDh9jNvANOVXxeB7PGcmvpVL_o1.m0mjE85-zx23QEbyqtSgGA" # This is used to refresh the authentication
}

from revChatGPT.revChatGPT import Chatbot
import json

chatbot = Chatbot(config, conversation_id=None)

def clear():
    chatbot.reset_chat() # Forgets conversation
    chatbot.refresh_session() # Uses the session_token to get a new bearer token

clear()

def ask(prompt: str) -> str:
    resp = chatbot.get_chat_response(prompt, output="text") # Sends a request to the API and returns the response by OpenAI
    res = "blank"
    for x in resp:
        print(x)
        res += str(x)
    return res # type: ignore # The message sent by the response
# resp['conversation_id'] # The current conversation id
# resp['parent_id'] # The ID of the response