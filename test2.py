from pyrogram import Client
import asyncio
import configparser


config = configparser.ConfigParser()
config.read("config.ini")


user_api_id=int(config["userbot"]["api_id"])
user_api_hash=config["userbot"]["api_hash"]
plugins_user=dict(root=config["userbot"]["plugins_root"])
workdir="sessions"


api_id=int(config["bot"]["api_id"])
api_hash=config["bot"]["api_hash"]
bot_token=config["bot"]["bot_token"]
plugins_bot=dict(root=config["bot"]["plugins_root"])
workdir="sessions"


#Client("userbot", api_id=user_api_id, api_hash=user_api_hash, plugins=plugins_user, workdir=workdir).run()
# async def main():
#     async with Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins_bot, workdir=workdir) as app:
#         user = await app.get_users('@inspector_gadget1')
#         print(user)
#         print(user.phone_number)
#         pass

# async def main():
#     async with Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins_bot, workdir=workdir) as app:
#         chat = await app.get_chat('-1001525422379')
#         print(chat)



# if chat.invite_link is None:
#     invite_link = await client.export_chat_invite_link(chat.id)
#     print(f"ExportInviteLink={invite_link}")
# else:
#     print(f"InvateLink={chat.invite_link}")

async def main():
    async with Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token, plugins=plugins_bot, workdir=workdir) as app:
        user = await app.get_users('355527991')
        print(user)     

# async def main():
#     async with Client("userbot", api_id=user_api_id, api_hash=user_api_hash, plugins=plugins_user, workdir=workdir) as app:
#         user = await app.get_users(355527991)
#         #print(user)
#         print(user.phone_number)
        #return chat.members_count
        

if __name__ == "__main__":
    asyncio.run(main())