import json

from llamaapi import LlamaAPI

from imapclient import IMAPClient
import mailparser


def get_imap_server(
    username: str, password: str, host: str = "imap.163.com"
) -> IMAPClient:
    server = IMAPClient(host, ssl=True, port=993)
    server.login(username, password)
    server.id_({"name": "IMAPClient"})
    return server


def fetch_email_summaries(
    server: IMAPClient, q: int, folder_name: str = "INBOX"
) -> str:
    try:
        emails_info = []
        server.select_folder(folder_name)
        messages = server.search(criteria="ALL", charset=None)
        email_ids = messages[::-1]

        limit = min(q, len(email_ids))
        for i in range(limit):
            email_id = email_ids[i]
            mail_content = server.fetch([email_id], ['RFC822'])[email_id][b'RFC822']
            mail_parsed = mailparser.parse_from_bytes(mail_content)
            emails_info.append(
                {
                    "Subject": mail_parsed.subject,
                    "From": mail_parsed.from_[0][1]  # sender: Assuming there's always a sender
                }
            )

        return json.dumps(emails_info, indent=2, ensure_ascii=False)
    except Exception as e:
        print("Err:", str(e))


if __name__ == "__main__":
    LLAMA_API_KEY = ...
    IMAP_USERNAME = ...
    IMAP_PASSWORD = ...
    # Refer to https://docs.llama-api.com/essentials/function#example-4-get-email-summary
    llama = LlamaAPI(LLAMA_API_KEY)  # Initialize the SDK
    model = "llama-70b-chat"
    imap_server = get_imap_server(IMAP_USERNAME, IMAP_PASSWORD)
    api_request_json = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Make a summary of my last e-mail."},
        ],
        "functions": [
            {
                "name": "fetch_email_summaries",
                "description": "Get the current value of emails",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "value": {
                            "type": "integer",
                            "description": "Quantity of emails"
                        },
                    },
                    "required": ["value"]
                }
            }
        ],
    }
    response = llama.run(api_request_json)
    output = response.json()['choices'][0]['message']
    print(output)
    infos = fetch_email_summaries(imap_server, q=output['function_call']['arguments']['value'])
    summarized_response = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Make a summary of my last e-mail."},
            {"role": "function", "name": output['function_call']['name'], "content": infos}
        ],
    }
    summarized_response = llama.run(summarized_response)
    print(summarized_response.json())
    # print(summarized_response.json()['choices'][0]['message']['content'])
