import pymongo
import datetime
import logging


logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

client = pymongo.MongoClient("mongodb://localhost:27017/")
mipt_db = client["mipt"]


def get_users_collection():
    collection = mipt_db["users"]
    collection.create_index("user_id", unique=True)
    return collection


def add_user(data: dict):

    logger.info(f"Add User: {data}")
    logger.info("Adding user ...")

    try:
        logger.info("The user data passed validation")
        user = {
            "user_id": data['userid'],
            "username": data["username"],
            "gender": data["gender"],
            "created": str(datetime.datetime.now()),
            "age": data["age"],
            "city": data["city"],
            "bio": data["bio"],
            "active": data["active"]
        }

        collection = get_users_collection()
        collection.insert_one(user)
        return f"Successfully added user: {user['username']}"
    except Exception as error:
        return f"Error {str(error)}"


def list_users():
    try:
        logger.info("listing users")
        collection = mipt_db["users"]
        users_list = list(collection.find({}, {"_id": 0}))
        if len(users_list) == 0:
            logger.warning("The users list is empty")
        return users_list
    except Exception as error:
        logger.error(str(error))
        return str(error)


def list_chats():
    collection_list = []
    for collection in mipt_db.list_collection_names():
        if collection == "users":
            continue

        collection_list.append({"chat": collection})

    return collection_list


def add_user_to_group(data):
    '''Will add users to group. If property doesn't exist than it will be created.'''
    try:
        user_id = data["user_id"]
        new_group = data["new_group"]
        collection = get_users_collection()
        logger.info(f"Adding {user_id} to {new_group}")
        '''Prevent from creating new user'''
        if collection.count_documents({'user_id': str(user_id)}, limit=1) == 0:
            return "The user doesn't exist"

        collection.update_one({'user_id': user_id}, {
                              "$set": {"group": new_group}}, upsert=True)
        return f"Success. The user {user_id} added to the group {new_group}"
    except Exception as error:
        return str(error)


def list_all_groups():
    try:
        unique_group_dict_list = []

        logger.info("listing users")
        collection = get_users_collection()
        group_list = list(collection.find({}, {"_id": 0, "group": 1}))

        if len(group_list) == 0:
            logger.warning("there are no groups!")

        '''Make all values of list unique'''
        unique_list = list(
            set(val for dic in group_list for val in dic.values()))

        for group in unique_list:
            unique_group_dict_list.append({"groupkey": group})

        return unique_group_dict_list

    except Exception as error:
        return str(error)


def list_users_of_group(group_name, include_id={"_id": 0}):
    try:
        logger.info("listing users")
        collection = get_users_collection()
        users_list = list(collection.find(
            {"group": {"$eq": group_name}}, include_id))
        if len(users_list) == 0:
            logger.warning("The users list is empty")
        return users_list
    except Exception as error:
        logger.error(str(error))
        return str(error)


def add_new_chat(data):
    try:
        group_name = data["group"]
        new_chat = data["new_chat"]

        collection = mipt_db[new_chat]

        if collection.count_documents({'name': group_name}, limit=1) != 0:
            return f"Group `{group_name}` is already in the chat `{new_chat}`"

        collection.insert_one({"name": group_name})

        return f'''Successfuly added group {group_name} to chat {new_chat}.'''
    except Exception as error:
        logger.error(str(error))
        return str(error)


def list_all_groups_of_chat(chat):
    try:

        collection = mipt_db[chat]
        group_list = list(collection.find({}, {"_id": 0}))
        logger.info(str(group_list))
        if len(group_list) == 0:
            logger.warning("there are no groups!")

        return group_list

    except Exception as error:
        return str(error)


def check_chat_access(chat):
    '''Check if collection exists'''
    if chat not in mipt_db.list_collection_names():
        return f'''Chat `{chat}` doesn't exist'''

    groups_of_chat = list_all_groups_of_chat(chat=chat)
    users_of_chat = []
    for group_name in groups_of_chat:
        users_of_chat.append(list_users_of_group(
            group_name=group_name.get("name")))

    return users_of_chat
