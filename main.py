import json
import os
import vk_api

from time import time

from threading import Thread
from queue import Queue

vk = None
vk_tools = None

def handle_messages(q, directory="users"):
	while True:

		done = q.task_done
		dialog = q.get()

		messages = {
			"title": dialog["title"],
			"messages": getHistory(dialog["peer_id"])
		}

		save(messages, directory)

		done()

def _normalize_directory(directory):
	if not directory:
		return ""
	if directory[:1] == "/":
		directory = directory[1:]
	if directory[:-1] == "/":
		directory = directory[-1:]

	return directory

def save(dialog, directory="users"):
	directory = _normalize_directory(directory)

	if not os.path.exists(directory):
		os.mkdir(directory)

	print(dialog["title"])
	
	title = r"+".join(dialog["title"].replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").split())
	open(f"{directory}/{title}.json", "w").write(json.dumps(dialog["messages"]))

def getDialogs():
	data = vk_tools.get_all(method="messages.getConversations",
                            max_count=200)['items']
	for peer in data:
		peer_id = peer["conversation"]["peer"]["id"]
		typ = peer["conversation"]["peer"]["type"]
		title = ""

		if typ == "user":
			data = vk.method("users.get", {"user_ids": peer_id})
			title = data[0]['first_name'] + "_" + data[0]["last_name"]
    
		if typ == "group":
			title = vk.method("groups.getById", {"group_ids": -peer_id})[0]["name"]
        
		if typ == "chat":
			title = vk.method("messages.getConversationsById", {
				"peer_ids": peer_id
			})['items'][0]['chat_settings']['title']

		yield {
			"title": title,
			"peer_id": peer_id
		}

def getHistory(dialog_id):

	history = vk_tools.get_all(method="messages.getHistory",
								max_count=200,
								values={
									"peer_id": dialog_id
								})

	def pretty_message(message):
		return {
			"message_id": message["id"],
			"dialog_id": dialog_id,
			"fwd_messages": message["fwd_messages"],
			"text": message["text"],
			"attachments": message["attachments"]
        }

	start = time()
	messages = list(map(pretty_message, history['items']))
	end = time()
	print(end-start)
	return messages

def main():
	global vk, vk_tools

	threads = input("Введите желаемое кол-во потоков: ")
	token = input("Введите юзер токен vkapi: ")
	directory = input("Введите нужный каталог: ")

	vk = vk_api.VkApi(token=token)
	vk_tools = vk_api.tools.VkTools(vk)

	queue = Queue()

	for _ in range(int(threads)):
		t = Thread(target=handle_messages, args=(queue, directory))
		t.daemon = True
		t.start()

	for dialog in getDialogs():
		queue.put(dialog)

if __name__ == "__main__":
	main()